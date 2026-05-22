from typing import Any
from sqlmodel import Session
from repositories.admin import (
    create_admin,
    delete_admin,
    get_admin_by_id,
    get_all_admin,
    update_admin,
)


def list_admin(session: Session):
    return get_all_admin(session)


def get_admin(session: Session, item_id: Any):
    return get_admin_by_id(session, item_id)


def create_admin_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_admin(session, data)


def update_admin_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_admin(session, item_id, data)


def delete_admin_item(session: Session, item_id: Any):
    return delete_admin(session, item_id)
