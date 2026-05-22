from typing import Any, Dict
from sqlmodel import Session
from models import Message
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_message(session: Session):
    return get_all_items(session, Message)


def get_message_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Message, item_id)


def create_message(session: Session, data: Dict[str, Any]):
    return create_item(session, Message, data)


def update_message(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Message, item_id, data)


def delete_message(session: Session, item_id: Any):
    return delete_item(session, Message, item_id)
