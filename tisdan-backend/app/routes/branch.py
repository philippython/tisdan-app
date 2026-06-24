from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.branch import BranchCreate, BranchResponse
from app.services.branch import (
    create_branch_item,
    delete_branch_item,
    get_branch,
    list_branch,
    update_branch_item,
)

router = APIRouter(
    prefix="/branches",
    tags=["Branches"],
)


@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create_branch(payload: BranchCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    return create_branch_item(session, payload)


@router.get("/", response_model=List[BranchResponse])
def read_branchs(session: Session = Depends(get_session)):
    return list_branch(session)


@router.get("/{item_id}", response_model=BranchResponse)
def read_branch(item_id: str, session: Session = Depends(get_session)):
    item = get_branch(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=BranchResponse)
def update_branch(item_id: str, payload: BranchCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    item = update_branch_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    deleted = delete_branch_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
