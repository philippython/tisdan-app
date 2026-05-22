from typing import Any, Dict
from sqlmodel import Session
from models import Result
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_result(session: Session):
    return get_all_items(session, Result)


def get_result_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Result, item_id)


def create_result(session: Session, data: Dict[str, Any]):
    return create_item(session, Result, data)


def update_result(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Result, item_id, data)


def delete_result(session: Session, item_id: Any):
    return delete_item(session, Result, item_id)
