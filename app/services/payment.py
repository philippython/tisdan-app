from typing import Any
from sqlmodel import Session
from app.repositories.payment import (
    create_payment,
    delete_payment,
    get_payment_by_id,
    get_all_payment,
    update_payment,
)


def list_payment(session: Session):
    return get_all_payment(session)


def get_payment(session: Session, item_id: Any):
    return get_payment_by_id(session, item_id)


def create_payment_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_payment(session, data)


def update_payment_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_payment(session, item_id, data)


def delete_payment_item(session: Session, item_id: Any):
    return delete_payment(session, item_id)
