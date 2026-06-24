from typing import Any, Dict
from sqlmodel import Session
from app.models import Customer
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_customers(session: Session):
    return get_all_items(session, Customer)


def get_customer_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Customer, item_id)


def create_customer(session: Session, data: Dict[str, Any]):
    return create_item(session, Customer, data)


def update_customer(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Customer, item_id, data)


def delete_customer(session: Session, item_id: Any):
    return delete_item(session, Customer, item_id)
