from typing import Any
from sqlmodel import Session
from app.repositories.staff import (
    create_staff,
    delete_staff,
    get_staff_by_id,
    get_all_staff,
    update_staff,
)


def list_staff(session: Session):
    return get_all_staff(session)


def get_staff(session: Session, item_id: Any):
    return get_staff_by_id(session, item_id)


def create_staff_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_staff(session, data)


def update_staff_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_staff(session, item_id, data)


def delete_staff_item(session: Session, item_id: Any):
    return delete_staff(session, item_id)
