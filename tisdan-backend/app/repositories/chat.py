from typing import Any, Dict
from sqlmodel import Session
from app.models import Chat
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_chat(session: Session):
    return get_all_items(session, Chat)


def get_chat_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Chat, item_id)


def create_chat(session: Session, data: Dict[str, Any]):
    return create_item(session, Chat, data)


def update_chat(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Chat, item_id, data)


def delete_chat(session: Session, item_id: Any):
    return delete_item(session, Chat, item_id)
