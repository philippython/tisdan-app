from typing import Any, Dict
from sqlmodel import Session
from app.models import BroadcastGeneral
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_broadcast_general(session: Session):
    return get_all_items(session, BroadcastGeneral)


def get_broadcast_general_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, BroadcastGeneral, item_id)


def create_broadcast_general(session: Session, data: Dict[str, Any]):
    return create_item(session, BroadcastGeneral, data)


def update_broadcast_general(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, BroadcastGeneral, item_id, data)


def delete_broadcast_general(session: Session, item_id: Any):
    return delete_item(session, BroadcastGeneral, item_id)
