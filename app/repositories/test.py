from typing import Any, Dict
from sqlmodel import Session
from models import Test
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_test(session: Session):
    return get_all_items(session, Test)


def get_test_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Test, item_id)


def create_test(session: Session, data: Dict[str, Any]):
    return create_item(session, Test, data)


def update_test(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Test, item_id, data)


def delete_test(session: Session, item_id: Any):
    return delete_item(session, Test, item_id)
