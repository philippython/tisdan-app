import traceback
from typing import Any
from sqlmodel import Session
from app.repositories.broadcast_general import (
    create_broadcast_general,
    delete_broadcast_general,
    get_broadcast_general_by_id,
    get_all_broadcast_general,
    update_broadcast_general,
)
from app.utils.bot_notify import queue_whatsapp
from app.services.recipients import client_phones


def list_broadcast_general(session: Session):
    return sorted(get_all_broadcast_general(session), key=lambda b: b.created_at, reverse=True)


def get_broadcast_general(session: Session, item_id: Any):
    return get_broadcast_general_by_id(session, item_id)


def _send_to_all_clients(session: Session, title: str, message: str) -> None:
    try:
        queue_whatsapp(client_phones(session), f"*{title}*\n\n{message}\n\n— Tisdan Care")
    except Exception:
        # Do not fail the primary operation if notifications fail,
        # but always log so failures are visible instead of silent.
        traceback.print_exc()


def create_broadcast_general_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    item = create_broadcast_general(session, data)
    _send_to_all_clients(session, item.title or "Announcement", item.message or "")
    return item


def update_broadcast_general_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    item = update_broadcast_general(session, item_id, data)
    if item is None:
        return None
    _send_to_all_clients(session, item.title or "Announcement", item.message or "")
    return item


def delete_broadcast_general_item(session: Session, item_id: Any):
    return delete_broadcast_general(session, item_id)
