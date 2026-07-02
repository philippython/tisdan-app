from typing import Any
from sqlmodel import Session
from app.models import Branch
from app.repositories.branch_schedule import (
    create_branch_schedule,
    delete_branch_schedule,
    get_branch_schedule_by_id,
    get_all_branch_schedule,
    update_branch_schedule,
)


def _enrich_branch_schedule(session: Session, item):
    if item is None:
        return item

    if getattr(item, "branch_id", None):
        branch = session.get(Branch, item.branch_id)
        if branch and getattr(branch, "name", None):
            item.branch_name = branch.name

    return item


def list_branch_schedule(session: Session):
    return [_enrich_branch_schedule(session, item) for item in get_all_branch_schedule(session)]


def get_branch_schedule(session: Session, item_id: Any):
    return _enrich_branch_schedule(session, get_branch_schedule_by_id(session, item_id))


def create_branch_schedule_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_branch_schedule(session, data)


def update_branch_schedule_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_branch_schedule(session, item_id, data)


def delete_branch_schedule_item(session: Session, item_id: Any):
    return delete_branch_schedule(session, item_id)
