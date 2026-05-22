from typing import Any
from sqlmodel import Session
from repositories.message import (
    create_message,
    delete_message,
    get_message_by_id,
    get_all_message,
    update_message,
)


def list_message(session: Session):
    return get_all_message(session)


def get_message(session: Session, item_id: Any):
    return get_message_by_id(session, item_id)


def create_message_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_message(session, data)


def update_message_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_message(session, item_id, data)


def delete_message_item(session: Session, item_id: Any):
    return delete_message(session, item_id)
