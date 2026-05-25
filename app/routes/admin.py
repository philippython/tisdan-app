from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.routes.dependencies import get_session
from app.schemas.admin import AdminCreate, AdminResponse
from app.services.admin import (
    create_admin_item,
    delete_admin_item,
    get_admin,
    list_admin,
    update_admin_item,
)

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(payload: AdminCreate, session: Session = Depends(get_session)):
    return create_admin_item(session, payload)


@router.get("/", response_model=List[AdminResponse])
def read_admins(session: Session = Depends(get_session)):
    return list_admin(session)


@router.get("/{item_id}", response_model=AdminResponse)
def read_admin(item_id: str, session: Session = Depends(get_session)):
    item = get_admin(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=AdminResponse)
def update_admin(item_id: str, payload: AdminCreate, session: Session = Depends(get_session)):
    item = update_admin_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_admin_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
