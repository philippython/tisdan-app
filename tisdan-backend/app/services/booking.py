from typing import Any
from sqlmodel import Session
from app.repositories.booking import (
    create_booking,
    delete_booking,
    get_booking_by_id,
    get_all_booking,
    update_booking,
)
from app.utils.bot_notify import send_whatsapp_via_bot, format_phone
from app.models import Booking, Customer, User, Branch, Test
from app.schemas.booking import BookingResponse
from sqlmodel import select


def _enrich_booking(session: Session, item: Booking):
    if item is None:
        return None

    user_full_name = None
    test_name = None
    branch_name = None

    if getattr(item, "user_id", None):
        user = session.get(User, item.user_id)
        if user and getattr(user, "full_name", None):
            user_full_name = user.full_name

    if getattr(item, "test_id", None):
        test = session.get(Test, item.test_id)
        if test and getattr(test, "name", None):
            test_name = test.name

    if getattr(item, "branch_id", None):
        branch = session.get(Branch, item.branch_id)
        if branch and getattr(branch, "name", None):
            branch_name = branch.name

    customer_full_name = None
    if getattr(item, "customer_id", None):
        customer = session.get(Customer, item.customer_id)
        if customer and getattr(customer, "full_name", None):
            customer_full_name = customer.full_name

    return BookingResponse(
        id=item.id,
        booking_date=item.booking_date,
        status=item.status,
        user_id=item.user_id,
        customer_id=item.customer_id,
        test_id=item.test_id,
        branch_id=item.branch_id,
        user_full_name=user_full_name,
        customer_full_name=customer_full_name,
        test_name=test_name,
        branch_name=branch_name,
    )


def list_booking(session: Session):
    return [_enrich_booking(session, item) for item in get_all_booking(session)]


def get_booking(session: Session, item_id: Any):
    return _enrich_booking(session, get_booking_by_id(session, item_id))


def create_booking_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_booking(session, data)

    # notify customer and admins about new booking
    try:
        phones = []
        if item.customer_id:
            cust = session.get(Customer, item.customer_id)
            if cust and cust.phone_number:
                phones.append(cust.phone_number)
        if item.user_id:
            user = session.get(User, item.user_id)
            if user and getattr(user, "phone_number", None):
                phones.append(user.phone_number)

        # admin/staff recipients
        stmt = select(User).where((User.role == "ADMIN") | (User.role == "STAFF"))
        for admin in session.exec(stmt):
            if getattr(admin, "phone_number", None):
                phones.append(admin.phone_number)

        # build message
        branch = session.get(Branch, item.branch_id) if getattr(item, "branch_id", None) else None
        test = session.get(Test, item.test_id) if getattr(item, "test_id", None) else None
        body = (
            "📅 *New Booking*\n\n"
            f"Booking ID: {str(item.id)}\n"
            f"Branch: {getattr(branch, 'name', 'N/A')}\n"
            f"Test: {getattr(test, 'name', 'N/A')}\n"
            f"Date: {getattr(item, 'booking_date', '')}\n\n"
            "Please contact the clinic for details. — Tisdan Care"
        )

        for p in set(phones):
            to = format_phone(p)
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return _enrich_booking(session, item)


def update_booking_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_booking(session, item_id, data)
    return _enrich_booking(session, item)


def delete_booking_item(session: Session, item_id: Any):
    return delete_booking(session, item_id)
