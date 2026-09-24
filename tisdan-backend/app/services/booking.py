import traceback
from typing import Any
from sqlmodel import Session
from app.repositories.booking import (
    create_booking,
    delete_booking,
    get_booking_by_id,
    get_all_booking,
    update_booking,
)
from app.utils.bot_notify import queue_whatsapp
from app.models import Booking, Customer, User, Branch, Test
from app.schemas.booking import BookingResponse
from app.services.recipients import booking_patient, staff_phones


def _enrich_booking(session: Session, item: Booking):
    if item is None:
        return None

    user = session.get(User, item.user_id) if item.user_id else None
    customer = session.get(Customer, item.customer_id) if item.customer_id else None
    test = session.get(Test, item.test_id) if item.test_id else None
    branch = session.get(Branch, item.branch_id) if item.branch_id else None
    patient_name, patient_phone = booking_patient(session, item)

    return BookingResponse(
        id=item.id,
        booking_date=item.booking_date,
        status=item.status,
        user_id=item.user_id,
        customer_id=item.customer_id,
        test_id=item.test_id,
        branch_id=item.branch_id,
        user_full_name=user.full_name if user else None,
        customer_full_name=customer.full_name if customer else None,
        patient_name=patient_name,
        patient_phone=patient_phone,
        test_name=test.name if test else None,
        test_price=test.price if test else None,
        branch_name=branch.name if branch else None,
    )


def list_booking(session: Session):
    items = sorted(get_all_booking(session), key=lambda b: b.booking_date, reverse=True)
    return [_enrich_booking(session, item) for item in items]


def get_booking(session: Session, item_id: Any):
    return _enrich_booking(session, get_booking_by_id(session, item_id))


def create_booking_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    item = create_booking(session, data)
    enriched = _enrich_booking(session, item)

    # notify the patient and admins/staff about the new booking
    try:
        body = (
            "📅 *New Booking*\n\n"
            f"Booking ID: {item.id}\n"
            f"Patient: {enriched.patient_name or 'N/A'}\n"
            f"Branch: {enriched.branch_name or 'N/A'}\n"
            f"Test: {enriched.test_name or 'N/A'}\n"
            f"Date: {item.booking_date:%d %b %Y, %H:%M}\n\n"
            "Please contact the clinic for details. — Tisdan Care"
        )
        phones = [enriched.patient_phone] + staff_phones(session)
        queue_whatsapp(phones, body)
    except Exception:
        traceback.print_exc()

    return enriched


_STATUS_MESSAGES = {
    "CONFIRMED": "✅ Your booking has been *confirmed*.",
    "CANCELLED": "❌ Your booking has been *cancelled*. Reply to this message if this is unexpected.",
    "COMPLETED": "🏁 Your visit is marked *completed*. Your result will be sent here once it is released.",
}


def update_booking_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    existing = get_booking_by_id(session, item_id)
    old_status = existing.status if existing else None

    item = update_booking(session, item_id, data)
    enriched = _enrich_booking(session, item)

    if item is not None and item.status != old_status and item.status in _STATUS_MESSAGES:
        try:
            body = (
                f"{_STATUS_MESSAGES[item.status]}\n\n"
                f"Test: {enriched.test_name or 'N/A'}\n"
                f"Branch: {enriched.branch_name or 'N/A'}\n"
                f"Date: {item.booking_date:%d %b %Y, %H:%M}\n"
                f"Reference: {item.id}\n\n— Tisdan Care"
            )
            queue_whatsapp([enriched.patient_phone], body)
        except Exception:
            traceback.print_exc()

    return enriched


def delete_booking_item(session: Session, item_id: Any):
    return delete_booking(session, item_id)
