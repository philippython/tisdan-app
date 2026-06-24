from typing import Any
from sqlmodel import Session
from app.repositories.chat import (
    create_chat,
    delete_chat,
    get_chat_by_id,
    get_all_chat,
    update_chat,
)


def list_chat(session: Session):
    return get_all_chat(session)


def get_chat(session: Session, item_id: Any):
    return get_chat_by_id(session, item_id)


def create_chat_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_chat(session, data)


def update_chat_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_chat(session, item_id, data)


def delete_chat_item(session: Session, item_id: Any):
    return delete_chat(session, item_id)
