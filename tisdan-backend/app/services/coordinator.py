from typing import Any, Optional
from sqlmodel import Session, select
from app.models import Coordinator, Referral, User
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

    result = item.model_dump()
    if getattr(item, "user_id", None):
        user = session.get(User, item.user_id)
        if user and getattr(user, "full_name", None):
            result["user_full_name"] = user.full_name
    result["referral_count"] = len(
        session.exec(select(Referral.id).where(Referral.coordinator_id == item.id)).all()
    )

    return result


def list_coordinator(session: Session, user_id: Optional[Any] = None):
    items = get_all_coordinator(session)
    if user_id is not None:
        items = [c for c in items if c.user_id == user_id]
    return [_enrich_coordinator(session, item) for item in items]


def get_coordinator(session: Session, item_id: Any):
    return _enrich_coordinator(session, get_coordinator_by_id(session, item_id))


def get_coordinator_by_code(session: Session, code: str):
    stmt = select(Coordinator).where(Coordinator.referral_code == code)
    return _enrich_coordinator(session, session.exec(stmt).first())


def create_coordinator_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    return _enrich_coordinator(session, create_coordinator(session, data))


def update_coordinator_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    return _enrich_coordinator(session, update_coordinator(session, item_id, data))


def delete_coordinator_item(session: Session, item_id: Any):
    return delete_coordinator(session, item_id)
