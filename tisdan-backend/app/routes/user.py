from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.user import UserCreate, UserResponse
from app.services.user import (
    create_user_item,
    delete_user_item,
    get_user,
    list_user,
    update_user_item,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    return create_user_item(session, payload)


@router.get("/", response_model=List[UserResponse])
def read_users(session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    return list_user(session)


@router.get("/{item_id}", response_model=UserResponse)
def read_user(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    item = get_user(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=UserResponse)
def update_user(item_id: str, payload: UserCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN))):
    item = update_user_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN))):
    deleted = delete_user_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None