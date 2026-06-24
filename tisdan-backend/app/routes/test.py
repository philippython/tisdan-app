from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.test import TestCreate, TestResponse
from app.services.test import (
    create_test_item,
    delete_test_item,
    get_test,
    list_test,
    update_test_item,
)

router = APIRouter(
    prefix="/tests",
    tags=["Tests"],
)


@router.post("/", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
def create_test(payload: TestCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN))):
    return create_test_item(session, payload)


@router.get("/", response_model=List[TestResponse])
def read_tests(session: Session = Depends(get_session)):
    return list_test(session)


@router.get("/{item_id}", response_model=TestResponse)
def read_test(item_id: str, session: Session = Depends(get_session)):
    item = get_test(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=TestResponse)
def update_test(item_id: str, payload: TestCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    item = update_test_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN))):
    deleted = delete_test_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
