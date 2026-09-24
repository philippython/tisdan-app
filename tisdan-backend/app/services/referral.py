from typing import Any, Optional
from sqlmodel import Session, select
from app.models import Coordinator, User
from app.repositories.referral import (
    create_referral,
    delete_referral,
    get_referral_by_id,
    get_all_referral,
    update_referral,
)


def _enrich_referral(session: Session, item):
    if item is None:
        return item

    result = item.model_dump()
    coordinator = session.get(Coordinator, item.coordinator_id)
    if coordinator:
        result["coordinator_code"] = coordinator.referral_code
        result["coordinator_user_id"] = coordinator.user_id
        user = session.get(User, coordinator.user_id)
        if user and getattr(user, "full_name", None):
            result["coordinator_name"] = user.full_name

    return result


def list_referral(session: Session, coordinator_user_id: Optional[Any] = None):
    items = sorted(get_all_referral(session), key=lambda r: r.created_at, reverse=True)
    enriched = [_enrich_referral(session, item) for item in items]
    if coordinator_user_id is not None:
        enriched = [r for r in enriched if r.get("coordinator_user_id") == coordinator_user_id]
    return enriched


def get_referral(session: Session, item_id: Any):
    return _enrich_referral(session, get_referral_by_id(session, item_id))


def _resolve_coordinator_id(session: Session, data: dict):
    """Allow the caller (e.g. the WhatsApp bot) to identify the coordinator
    either by UUID (coordinator_id) or by their referral_code (coordinator_code)."""
    if data.get("coordinator_id"):
        return data["coordinator_id"]

    code = data.pop("coordinator_code", None)
    if code:
        stmt = select(Coordinator).where(Coordinator.referral_code == code)
        coordinator = session.exec(stmt).first()
        if coordinator:
            return coordinator.id

    return None


def create_referral_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    coordinator_id = _resolve_coordinator_id(session, data)
    if not coordinator_id:
        raise ValueError("Unknown coordinator: provide a valid coordinator_id or coordinator_code")

    data["coordinator_id"] = coordinator_id
    data.pop("coordinator_code", None)
    item = create_referral(session, data)
    return _enrich_referral(session, item)


def update_referral_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    if "coordinator_code" in data or data.get("coordinator_id"):
        coordinator_id = _resolve_coordinator_id(session, data)
        if coordinator_id:
            data["coordinator_id"] = coordinator_id
    data.pop("coordinator_code", None)
    item = update_referral(session, item_id, data)
    return _enrich_referral(session, item)


def delete_referral_item(session: Session, item_id: Any):
    return delete_referral(session, item_id)
