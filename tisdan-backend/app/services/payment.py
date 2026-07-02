from typing import Any
from sqlmodel import Session, select
from app.repositories.payment import (
    create_payment,
    delete_payment,
    get_payment_by_id,
    get_all_payment,
    update_payment,
)
from app.utils.bot_notify import send_whatsapp_via_bot, format_phone
from app.models import Booking, Customer, User
from app.enums.payment_status_enum import PaymentStatus


def list_payment(session: Session):
    return get_all_payment(session)


def get_payment(session: Session, item_id: Any):
    return get_payment_by_id(session, item_id)


def create_payment_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_payment(session, data)

    # notify customer and admins with receipt
    try:
        phones = []
        booking_id = data.get("booking_id") or getattr(item, "booking_id", None)
        if booking_id:
            booking = session.get(Booking, booking_id)
            if booking:
                if booking.customer_id:
                    cust = session.get(Customer, booking.customer_id)
                    if cust and cust.phone_number:
                        phones.append(cust.phone_number)
                if booking.user_id:
                    user = session.get(User, booking.user_id)
                    if user and getattr(user, "phone_number", None):
                        phones.append(user.phone_number)

        stmt = select(User).where((User.role == "ADMIN") | (User.role == "STAFF"))
        for admin in session.exec(stmt):
            if getattr(admin, "phone_number", None):
                phones.append(admin.phone_number)

        amount = data.get("amount") or getattr(item, "amount", "")
        body = (
            "💳 *Payment Received*\n\n"
            f"Amount: {amount}\n"
            f"Reference: {str(getattr(item, 'id', ''))}\n\n"
            "Thank you. — Tisdan Care"
        )
        for p in set(phones):
            to = format_phone(p)
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def update_payment_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_payment(session, item_id, data)
    return item


def delete_payment_item(session: Session, item_id: Any):
    return delete_payment(session, item_id)
