from typing import Any
from sqlmodel import Session
from repositories.broadcast_general import (
    create_broadcast_general,
    delete_broadcast_general,
    get_broadcast_general_by_id,
    get_all_broadcast_general,
    update_broadcast_general,
)


def list_broadcast_general(session: Session):
    return get_all_broadcast_general(session)


def get_broadcast_general(session: Session, item_id: Any):
    return get_broadcast_general_by_id(session, item_id)


def create_broadcast_general_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_broadcast_general(session, data)


def update_broadcast_general_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_broadcast_general(session, item_id, data)


def delete_broadcast_general_item(session: Session, item_id: Any):
    return delete_broadcast_general(session, item_id)
