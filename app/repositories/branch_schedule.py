from typing import Any, Dict
from sqlmodel import Session
from models import BranchSchedule
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_branch_schedule(session: Session):
    return get_all_items(session, BranchSchedule)


def get_branch_schedule_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, BranchSchedule, item_id)


def create_branch_schedule(session: Session, data: Dict[str, Any]):
    return create_item(session, BranchSchedule, data)


def update_branch_schedule(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, BranchSchedule, item_id, data)


def delete_branch_schedule(session: Session, item_id: Any):
    return delete_item(session, BranchSchedule, item_id)
