from typing import Any
from sqlmodel import Session
from app.models import Branch
from app.schemas.branch_schedule import BranchScheduleResponse
from app.repositories.branch_schedule import (
    create_branch_schedule,
    delete_branch_schedule,
    get_branch_schedule_by_id,
    get_all_branch_schedule,
    update_branch_schedule,
)


_DAY_ORDER = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


def _enrich_branch_schedule(session: Session, item):
    if item is None:
        return item

    response = BranchScheduleResponse.model_validate(item)
    branch = session.get(Branch, item.branch_id) if item.branch_id else None
    response.branch_name = branch.name if branch else None
    return response


def _sort_key(item):
    day = (item.day or "").upper()
    return (str(item.branch_id), _DAY_ORDER.index(day) if day in _DAY_ORDER else 99)


def list_branch_schedule(session: Session):
    items = sorted(get_all_branch_schedule(session), key=_sort_key)
    return [_enrich_branch_schedule(session, item) for item in items]


def get_branch_schedule(session: Session, item_id: Any):
    return _enrich_branch_schedule(session, get_branch_schedule_by_id(session, item_id))


def create_branch_schedule_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    return _enrich_branch_schedule(session, create_branch_schedule(session, data))


def update_branch_schedule_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    return _enrich_branch_schedule(session, update_branch_schedule(session, item_id, data))


def delete_branch_schedule_item(session: Session, item_id: Any):
    return delete_branch_schedule(session, item_id)
