import traceback
from typing import Any
from sqlmodel import Session
from app.repositories.test import (
    create_test,
    delete_test,
    get_test_by_id,
    get_all_test,
    update_test,
)
from app.utils.bot_notify import queue_whatsapp
from app.services.recipients import client_phones


def list_test(session: Session):
    return sorted(get_all_test(session), key=lambda t: t.name.lower())


def get_test(session: Session, item_id: Any):
    return get_test_by_id(session, item_id)


def _announce(session: Session, body: str) -> None:
    try:
        queue_whatsapp(client_phones(session), body)
    except Exception:
        traceback.print_exc()


def create_test_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    item = create_test(session, data)
    _announce(
        session,
        f"🧪 *New Test Available*\n\n{item.name} — ₦{item.price:,.0f}\n\n"
        "Book at any Tisdan branch or reply here. — Tisdan Care",
    )
    return item


def update_test_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    existing = get_test_by_id(session, item_id)
    if existing is None:
        return None
    old_price = existing.price

    item = update_test(session, item_id, data)
    # only announce changes customers care about
    if item.price != old_price:
        _announce(
            session,
            f"🔄 *Price Update*\n\n{item.name} — now ₦{item.price:,.0f}\n\n"
            "Reply here to book. — Tisdan Care",
        )
    return item


def delete_test_item(session: Session, item_id: Any):
    return delete_test(session, item_id)
