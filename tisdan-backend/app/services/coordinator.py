from typing import Any
from sqlmodel import Session
from app.models import User
from app.repositories.coordinator import (
    create_coordinator,
    delete_coordinator,
    get_coordinator_by_id,
    get_all_coordinator,
    update_coordinator,
)


def _enrich_coordinator(session: Session, item):
    if item is None:
        return item

    result = item.dict()
    if getattr(item, "user_id", None):
        user = session.get(User, item.user_id)
        if user and getattr(user, "full_name", None):
            result["user_full_name"] = user.full_name

    return result


def list_coordinator(session: Session):
    return [_enrich_coordinator(session, item) for item in get_all_coordinator(session)]


def get_coordinator(session: Session, item_id: Any):
    return _enrich_coordinator(session, get_coordinator_by_id(session, item_id))


def create_coordinator_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_coordinator(session, data)


def update_coordinator_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_coordinator(session, item_id, data)


def delete_coordinator_item(session: Session, item_id: Any):
    return delete_coordinator(session, item_id)
