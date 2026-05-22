from typing import Any, Dict
from sqlmodel import Session
from models import Client
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_client(session: Session):
    return get_all_items(session, Client)


def get_client_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Client, item_id)


def create_client(session: Session, data: Dict[str, Any]):
    return create_item(session, Client, data)


def update_client(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Client, item_id, data)


def delete_client(session: Session, item_id: Any):
    return delete_item(session, Client, item_id)
