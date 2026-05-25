from typing import Any
from sqlmodel import Session
from app.repositories.user import (
    create_user,
    delete_user,
    get_user_by_id,
    get_all_user,
    update_user,
)


def list_user(session: Session):
    return get_all_user(session)


def get_user(session: Session, item_id: Any):
    return get_user_by_id(session, item_id)


def create_user_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_user(session, data)


def update_user_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_user(session, item_id, data)


def delete_user_item(session: Session, item_id: Any):
    return delete_user(session, item_id)
