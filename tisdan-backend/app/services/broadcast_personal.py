from typing import Any
from sqlmodel import Session
from app.repositories.broadcast_personal import (
    create_broadcast_personal,
    delete_broadcast_personal,
    get_broadcast_personal_by_id,
    get_all_broadcast_personal,
    update_broadcast_personal,
)
from app.utils.bot_notify import send_whatsapp_via_bot, format_phone
from app.models import User


def list_broadcast_personal(session: Session):
    return get_all_broadcast_personal(session)


def get_broadcast_personal(session: Session, item_id: Any):
    return get_broadcast_personal_by_id(session, item_id)


def create_broadcast_personal_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_broadcast_personal(session, data)

    try:
        user = session.get(User, data["user_id"])
        if user and getattr(user, "phone_number", None):
            to = format_phone(user.phone_number)
            body = (
                "📩 *Personal Message from Tisdan Care*\n\n"
                f"{data.get('message', '')}\n\n"
                "Reply to this WhatsApp if you need help."
            )
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def update_broadcast_personal_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_broadcast_personal(session, item_id, data)
    if item is None:
        return None

    try:
        user = session.get(User, data.get("user_id", getattr(item, "user_id", None)))
        if user and getattr(user, "phone_number", None):
            to = format_phone(user.phone_number)
            body = (
                "🔄 *Updated Personal Message from Tisdan Care*\n\n"
                f"{data.get('message', getattr(item, 'message', ''))}\n\n"
                "Reply to this WhatsApp if you need help."
            )
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def delete_broadcast_personal_item(session: Session, item_id: Any):
    return delete_broadcast_personal(session, item_id)
