from typing import Any
from sqlmodel import Session
from app.repositories.branch_schedule import (
    create_branch_schedule,
    delete_branch_schedule,
    get_branch_schedule_by_id,
    get_all_branch_schedule,
    update_branch_schedule,
)


def list_branch_schedule(session: Session):
    return get_all_branch_schedule(session)


def get_branch_schedule(session: Session, item_id: Any):
    return get_branch_schedule_by_id(session, item_id)


def create_branch_schedule_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_branch_schedule(session, data)


def update_branch_schedule_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_branch_schedule(session, item_id, data)


def delete_branch_schedule_item(session: Session, item_id: Any):
    return delete_branch_schedule(session, item_id)
