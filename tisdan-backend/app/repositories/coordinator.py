from typing import Any, Dict
from sqlmodel import Session
from app.models import Coordinator
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_coordinator(session: Session):
    return get_all_items(session, Coordinator)


def get_coordinator_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Coordinator, item_id)


def create_coordinator(session: Session, data: Dict[str, Any]):
    return create_item(session, Coordinator, data)


def update_coordinator(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Coordinator, item_id, data)


def delete_coordinator(session: Session, item_id: Any):
    return delete_item(session, Coordinator, item_id)
