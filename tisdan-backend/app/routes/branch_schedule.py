from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.branch_schedule import BranchScheduleCreate, BranchScheduleResponse
from app.services.branch_schedule import (
    create_branch_schedule_item,
    delete_branch_schedule_item,
    get_branch_schedule,
    list_branch_schedule,
    update_branch_schedule_item,
)

router = APIRouter(
    prefix="/branch-schedules",
    tags=["BranchSchedules"],
)


@router.post("/", response_model=BranchScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_branch_schedule(payload: BranchScheduleCreate, session: Session = Depends(get_session)):
    return create_branch_schedule_item(session, payload)


@router.get("/", response_model=List[BranchScheduleResponse])
def read_branch_schedules(session: Session = Depends(get_session)):
    return list_branch_schedule(session)


@router.get("/{item_id}", response_model=BranchScheduleResponse)
def read_branch_schedule(item_id: str, session: Session = Depends(get_session)):
    item = get_branch_schedule(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=BranchScheduleResponse)
def update_branch_schedule(item_id: str, payload: BranchScheduleCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    item = update_branch_schedule_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch_schedule(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    deleted = delete_branch_schedule_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
