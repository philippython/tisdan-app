from typing import Any
from sqlmodel import Session
from repositories.client import (
    create_client,
    delete_client,
    get_client_by_id,
    get_all_client,
    update_client,
)


def list_client(session: Session):
    return get_all_client(session)


def get_client(session: Session, item_id: Any):
    return get_client_by_id(session, item_id)


def create_client_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_client(session, data)


def update_client_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_client(session, item_id, data)


def delete_client_item(session: Session, item_id: Any):
    return delete_client(session, item_id)
