from typing import Any
from sqlmodel import Session
from app.repositories.branch import (
    create_branch,
    delete_branch,
    get_branch_by_id,
    get_all_branch,
    update_branch,
)


def list_branch(session: Session):
    return get_all_branch(session)


def get_branch(session: Session, item_id: Any):
    return get_branch_by_id(session, item_id)


def create_branch_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_branch(session, data)


def update_branch_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_branch(session, item_id, data)


def delete_branch_item(session: Session, item_id: Any):
    return delete_branch(session, item_id)
