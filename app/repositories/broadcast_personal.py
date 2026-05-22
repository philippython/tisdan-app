from typing import Any, Dict
from sqlmodel import Session
from models import BroadcastPersonal
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_broadcast_personal(session: Session):
    return get_all_items(session, BroadcastPersonal)


def get_broadcast_personal_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, BroadcastPersonal, item_id)


def create_broadcast_personal(session: Session, data: Dict[str, Any]):
    return create_item(session, BroadcastPersonal, data)


def update_broadcast_personal(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, BroadcastPersonal, item_id, data)


def delete_broadcast_personal(session: Session, item_id: Any):
    return delete_item(session, BroadcastPersonal, item_id)
