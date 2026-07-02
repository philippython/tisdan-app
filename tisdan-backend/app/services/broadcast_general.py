from typing import Any
from sqlmodel import Session
from app.repositories.broadcast_general import (
    create_broadcast_general,
    delete_broadcast_general,
    get_broadcast_general_by_id,
    get_all_broadcast_general,
    update_broadcast_general,
)
from app.utils.bot_notify import send_whatsapp_via_bot, format_phone
from app.models import Customer, User
from sqlmodel import select


def list_broadcast_general(session: Session):
    return get_all_broadcast_general(session)


def get_broadcast_general(session: Session, item_id: Any):
    return get_broadcast_general_by_id(session, item_id)


def create_broadcast_general_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_broadcast_general(session, data)

    # notify all customers and client users with phone numbers
    title = data.get("title") or "Announcement"
    message = data.get("message") or ""
    full = f"*{title}*\n\n{message}\n\n— Tisdan Care"

    # customers
    try:
        stmt = select(Customer).where(Customer.phone_number != None)
        for cust in session.exec(stmt):
            to = format_phone(cust.phone_number)
            if to:
                send_whatsapp_via_bot(to, full)

        # users with role CLIENT
        stmt2 = select(User).where(User.role == "CLIENT")
        for user in session.exec(stmt2):
            to = format_phone(user.phone_number)
            if to:
                send_whatsapp_via_bot(to, full)
    except Exception:
        # do not fail creation if notifications fail
        pass

    return item


def update_broadcast_general_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_broadcast_general(session, item_id, data)
    if item is None:
        return None

    # send update notification similar to create
    title = data.get("title") or getattr(item, "title", "Announcement")
    message = data.get("message") or getattr(item, "message", "")
    full = f"*{title}*\n\n{message}\n\n— Tisdan Care"
    try:
        stmt = select(Customer).where(Customer.phone_number != None)
        for cust in session.exec(stmt):
            to = format_phone(cust.phone_number)
            if to:
                send_whatsapp_via_bot(to, full)
        stmt2 = select(User).where(User.role == "CLIENT")
        for user in session.exec(stmt2):
            to = format_phone(user.phone_number)
            if to:
                send_whatsapp_via_bot(to, full)
    except Exception:
        pass

    return item


def delete_broadcast_general_item(session: Session, item_id: Any):
    return delete_broadcast_general(session, item_id)
