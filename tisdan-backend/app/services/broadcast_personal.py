from typing import Any
from sqlmodel import Session
from app.repositories.broadcast_personal import (
    create_broadcast_personal,
    delete_broadcast_personal,
    get_broadcast_personal_by_id,
    get_all_broadcast_personal,
    update_broadcast_personal,
)


def list_broadcast_personal(session: Session):
    return get_all_broadcast_personal(session)


def get_broadcast_personal(session: Session, item_id: Any):
    return get_broadcast_personal_by_id(session, item_id)


def create_broadcast_personal_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_broadcast_personal(session, data)


def update_broadcast_personal_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_broadcast_personal(session, item_id, data)


def delete_broadcast_personal_item(session: Session, item_id: Any):
    return delete_broadcast_personal(session, item_id)
