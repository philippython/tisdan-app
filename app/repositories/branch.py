from typing import Any, Dict
from sqlmodel import Session
from models import Branch
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_branch(session: Session):
    return get_all_items(session, Branch)


def get_branch_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Branch, item_id)


def create_branch(session: Session, data: Dict[str, Any]):
    return create_item(session, Branch, data)


def update_branch(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Branch, item_id, data)


def delete_branch(session: Session, item_id: Any):
    return delete_item(session, Branch, item_id)
