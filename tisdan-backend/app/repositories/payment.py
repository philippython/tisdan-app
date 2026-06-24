from typing import Any, Dict
from sqlmodel import Session
from app.models import Payment
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_payment(session: Session):
    return get_all_items(session, Payment)


def get_payment_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Payment, item_id)


def create_payment(session: Session, data: Dict[str, Any]):
    return create_item(session, Payment, data)


def update_payment(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Payment, item_id, data)


def delete_payment(session: Session, item_id: Any):
    return delete_item(session, Payment, item_id)
