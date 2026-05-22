from typing import Any, Dict
from sqlmodel import Session
from models import Staff
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_staff(session: Session):
    return get_all_items(session, Staff)


def get_staff_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Staff, item_id)


def create_staff(session: Session, data: Dict[str, Any]):
    return create_item(session, Staff, data)


def update_staff(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Staff, item_id, data)


def delete_staff(session: Session, item_id: Any):
    return delete_item(session, Staff, item_id)
