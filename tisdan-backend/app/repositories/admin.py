from typing import Any, Dict
from sqlmodel import Session
from app.models import Admin
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_admin(session: Session):
    return get_all_items(session, Admin)


def get_admin_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Admin, item_id)


def create_admin(session: Session, data: Dict[str, Any]):
    return create_item(session, Admin, data)


def update_admin(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Admin, item_id, data)


def delete_admin(session: Session, item_id: Any):
    return delete_item(session, Admin, item_id)
