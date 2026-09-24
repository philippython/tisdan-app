import hashlib
import hmac
import traceback
import uuid
from typing import Any, Optional
import requests
from sqlmodel import Session, select
from app.repositories.payment import (
    create_payment,
    delete_payment,
    get_payment_by_id,
    get_all_payment,
    update_payment,
)
from app.utils.bot_notify import format_phone, queue_whatsapp, send_whatsapp_via_bot
from app.models import Booking, Customer, Payment, User
from app.enums.payment_status_enum import PaymentStatus
from app.core.config import settings
from app.schemas.payment import PaymentResponse
from app.services.recipients import booking_patient_phones, staff_phones


def _enrich_payment(session: Session, item: Optional[Payment]):
    if item is None:
        return None
    payer = session.get(User, item.payer_id) if item.payer_id else None
    response = PaymentResponse.model_validate(item)
    response.payer_name = payer.full_name if payer else None
    return response


def list_payment(session: Session):
    items = sorted(get_all_payment(session), key=lambda p: p.created_at, reverse=True)
    return [_enrich_payment(session, item) for item in items]


def get_payment(session: Session, item_id: Any):
    return _enrich_payment(session, get_payment_by_id(session, item_id))


def _send_receipt(session: Session, item: Payment) -> None:
    """WhatsApp a receipt to the payer/patient and admins once paid."""
    try:
        payer = session.get(User, item.payer_id)
        phones = booking_patient_phones(session, item.booking_id)
        if payer and payer.phone_number:
            phones.append(payer.phone_number)
        phones += staff_phones(session)
        body = (
            "💳 *Payment Received*\n\n"
            f"Amount: {item.currency} {item.amount:,.2f}\n"
            f"Reference: {item.reference or item.id}\n\n"
            "Thank you. — Tisdan Care"
        )
        queue_whatsapp(phones, body)
    except Exception:
        traceback.print_exc()


def create_payment_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    item = create_payment(session, data)
    if item.status == PaymentStatus.COMPLETED:
        _send_receipt(session, item)
    return _enrich_payment(session, item)


def update_payment_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    existing = get_payment_by_id(session, item_id)
    if existing is None:
        return None
    was_completed = existing.status == PaymentStatus.COMPLETED
    item = update_payment(session, item_id, data)
    if item.status == PaymentStatus.COMPLETED and not was_completed:
        _send_receipt(session, item)
    return _enrich_payment(session, item)


def delete_payment_item(session: Session, item_id: Any):
    return delete_payment(session, item_id)


def initialize_payment(session: Session, payload: Any):
    """Create a PENDING payment record, start a Paystack transaction for it,
    and WhatsApp the resulting payment link to the payer.

    Returns a dict with the created payment plus the Paystack
    authorization_url (None if Paystack isn't configured or the call fails —
    the payment record is still created either way so it isn't lost).
    """
    data = payload.model_dump(exclude_none=True)
    reference = data.get("reference") or f"TSDN-{uuid.uuid4().hex[:10].upper()}"
    data["reference"] = reference
    data.setdefault("currency", "NGN")

    item = create_payment(session, data)

    payer = session.get(User, item.payer_id)
    email = getattr(payer, "email", None) or f"{item.payer_id}@tisdan.care"

    authorization_url = None
    access_code = None

    if settings.PAYSTACK_SECRET_KEY:
        try:
            resp = requests.post(
                f"{str(settings.PAYSTACK_BASE_URL).rstrip('/')}/transaction/initialize",
                headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
                json={
                    "email": email,
                    # Paystack expects the smallest currency unit (kobo for NGN)
                    "amount": int(round(item.amount * 100)),
                    "currency": item.currency,
                    "reference": reference,
                },
                timeout=10,
            )
            if resp.status_code == 200 and resp.json().get("status"):
                pdata = resp.json().get("data", {})
                authorization_url = pdata.get("authorization_url")
                access_code = pdata.get("access_code")
            else:
                print(f"Paystack initialize failed: HTTP {resp.status_code} - {resp.text}")
        except Exception:
            traceback.print_exc()
    else:
        print("Payment initialized without Paystack: PAYSTACK_SECRET_KEY is not set in tisdan-backend/.env")

    whatsapp_sent = False
    try:
        phone = getattr(payer, "phone_number", None)
        if not phone and item.booking_id:
            booking = session.get(Booking, item.booking_id)
            if booking and booking.customer_id:
                cust = session.get(Customer, booking.customer_id)
                if cust:
                    phone = cust.phone_number

        to = format_phone(phone)
        if to:
            link_line = f"Pay here: {authorization_url}\n\n" if authorization_url else ""
            body = (
                "💳 *Payment Requested*\n\n"
                f"Amount: {item.currency} {item.amount:,.2f}\n"
                f"Reference: {reference}\n\n"
                f"{link_line}"
                "— Tisdan Care"
            )
            whatsapp_sent = send_whatsapp_via_bot(to, body)
    except Exception:
        traceback.print_exc()

    return {
        "payment": _enrich_payment(session, item),
        "authorization_url": authorization_url,
        "access_code": access_code,
        "reference": reference,
        "whatsapp_sent": whatsapp_sent,
    }


def _get_by_reference(session: Session, reference: str) -> Optional[Payment]:
    return session.exec(select(Payment).where(Payment.reference == reference)).first()


def _apply_paystack_status(session: Session, item: Payment, paystack_status: str) -> Payment:
    new_status = {
        "success": PaymentStatus.COMPLETED,
        "failed": PaymentStatus.FAILED,
        "abandoned": PaymentStatus.FAILED,
        "reversed": PaymentStatus.FAILED,
    }.get(paystack_status)
    if new_status is None or item.status == new_status:
        return item
    was_completed = item.status == PaymentStatus.COMPLETED
    item = update_payment(session, item.id, {"status": new_status})
    if new_status == PaymentStatus.COMPLETED and not was_completed:
        _send_receipt(session, item)
    return item


def verify_payment(session: Session, reference: str):
    """Ask Paystack for the transaction's status and sync our record."""
    item = _get_by_reference(session, reference)
    if item is None:
        return None
    if not settings.PAYSTACK_SECRET_KEY:
        raise ValueError("PAYSTACK_SECRET_KEY is not configured")
    resp = requests.get(
        f"{str(settings.PAYSTACK_BASE_URL).rstrip('/')}/transaction/verify/{reference}",
        headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
        timeout=10,
    )
    if resp.status_code == 200 and resp.json().get("status"):
        item = _apply_paystack_status(session, item, resp.json()["data"].get("status"))
    return _enrich_payment(session, item)


def valid_paystack_signature(raw_body: bytes, signature: Optional[str]) -> bool:
    if not settings.PAYSTACK_SECRET_KEY or not signature:
        return False
    expected = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(), raw_body, hashlib.sha512
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def handle_paystack_event(session: Session, event: dict) -> None:
    data = event.get("data") or {}
    reference = data.get("reference")
    if not reference:
        return
    item = _get_by_reference(session, reference)
    if item is None:
        return
    if event.get("event") == "charge.success":
        _apply_paystack_status(session, item, "success")
    elif data.get("status"):
        _apply_paystack_status(session, item, data["status"])
