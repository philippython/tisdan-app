from typing import Any
from sqlmodel import Session
from app.repositories.booking import (
    create_booking,
    delete_booking,
    get_booking_by_id,
    get_all_booking,
    update_booking,
)


def list_booking(session: Session):
    return get_all_booking(session)


def get_booking(session: Session, item_id: Any):
    return get_booking_by_id(session, item_id)


def create_booking_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_booking(session, data)


def update_booking_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_booking(session, item_id, data)


def delete_booking_item(session: Session, item_id: Any):
    return delete_booking(session, item_id)
