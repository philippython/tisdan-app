from typing import Any
from sqlmodel import Session
from app.repositories.test import (
    create_test,
    delete_test,
    get_test_by_id,
    get_all_test,
    update_test,
)
from app.utils.bot_notify import send_whatsapp_via_bot, format_phone
from app.models import Customer, User
from sqlmodel import select


def list_test(session: Session):
    return get_all_test(session)


def get_test(session: Session, item_id: Any):
    return get_test_by_id(session, item_id)


def create_test_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_test(session, data)

    # notify customers/users about new test
    try:
        title = data.get("name", "New Test")
        price = data.get("price", "Contact for price")
        body = f"🧪 *New Test Available*\n\n{title} — {price}\n\nBook at any Tisdan branch or reply here. — Tisdan Care"

        stmt = select(Customer).where(Customer.phone_number != None)
        for cust in session.exec(stmt):
            to = format_phone(cust.phone_number)
            if to:
                send_whatsapp_via_bot(to, body)

        stmt2 = select(User).where(User.role == "CLIENT")
        for u in session.exec(stmt2):
            to = format_phone(u.phone_number)
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def update_test_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_test(session, item_id, data)
    if item is None:
        return None

    try:
        title = data.get("name") or getattr(item, "name", "Test")
        price = data.get("price") or getattr(item, "price", "Contact for price")
        body = f"🔄 *Test Updated*\n\n{title} — {price}\n\nSee updates on our site. — Tisdan Care"

        stmt = select(Customer).where(Customer.phone_number != None)
        for cust in session.exec(stmt):
            to = format_phone(cust.phone_number)
            if to:
                send_whatsapp_via_bot(to, body)

        stmt2 = select(User).where(User.role == "CLIENT")
        for u in session.exec(stmt2):
            to = format_phone(u.phone_number)
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def delete_test_item(session: Session, item_id: Any):
    return delete_test(session, item_id)
