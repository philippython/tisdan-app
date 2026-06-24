from typing import Any
from sqlmodel import Session
from app.repositories.customer import (
    create_customer,
    delete_customer,
    get_customer_by_id,
    get_all_customers,
    update_customer,
)


def list_customers(session: Session):
    return get_all_customers(session)


def get_customer(session: Session, item_id: Any):
    return get_customer_by_id(session, item_id)


def create_customer_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_customer(session, data)


def update_customer_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_customer(session, item_id, data)


def delete_customer_item(session: Session, item_id: Any):
    return delete_customer(session, item_id)
