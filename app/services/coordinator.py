from typing import Any
from sqlmodel import Session
from app.repositories.coordinator import (
    create_coordinator,
    delete_coordinator,
    get_coordinator_by_id,
    get_all_coordinator,
    update_coordinator,
)


def list_coordinator(session: Session):
    return get_all_coordinator(session)


def get_coordinator(session: Session, item_id: Any):
    return get_coordinator_by_id(session, item_id)


def create_coordinator_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_coordinator(session, data)


def update_coordinator_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_coordinator(session, item_id, data)


def delete_coordinator_item(session: Session, item_id: Any):
    return delete_coordinator(session, item_id)
