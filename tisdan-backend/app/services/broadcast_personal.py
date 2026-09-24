import traceback
from typing import Any
from sqlmodel import Session
from app.repositories.broadcast_personal import (
    create_broadcast_personal,
    delete_broadcast_personal,
    get_broadcast_personal_by_id,
    get_all_broadcast_personal,
    update_broadcast_personal,
)
from app.utils.bot_notify import queue_whatsapp
from app.models import BroadcastPersonal, User
from app.schemas.broadcast import BroadcastPersonalResponse


def _enrich(session: Session, item: BroadcastPersonal):
    if item is None:
        return None
    user = session.get(User, item.user_id)
    response = BroadcastPersonalResponse.model_validate(item)
    response.user_full_name = user.full_name if user else None
    return response


def list_broadcast_personal(session: Session):
    items = sorted(get_all_broadcast_personal(session), key=lambda b: b.created_at, reverse=True)
    return [_enrich(session, item) for item in items]


def get_broadcast_personal(session: Session, item_id: Any):
    return _enrich(session, get_broadcast_personal_by_id(session, item_id))


def _send(session: Session, item: BroadcastPersonal, heading: str) -> None:
    try:
        user = session.get(User, item.user_id)
        body = (
            f"{heading}\n\n"
            f"{item.message}\n\n"
            "Reply to this WhatsApp if you need help."
        )
        queue_whatsapp([user.phone_number if user else None], body)
    except Exception:
        # Do not fail the primary operation if notifications fail,
        # but always log so failures are visible instead of silent.
        traceback.print_exc()


def create_broadcast_personal_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    item = create_broadcast_personal(session, data)
    _send(session, item, "📩 *Personal Message from Tisdan Care*")
    return _enrich(session, item)


def update_broadcast_personal_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    item = update_broadcast_personal(session, item_id, data)
    if item is None:
        return None
    _send(session, item, "🔄 *Updated Personal Message from Tisdan Care*")
    return _enrich(session, item)


def delete_broadcast_personal_item(session: Session, item_id: Any):
    return delete_broadcast_personal(session, item_id)
