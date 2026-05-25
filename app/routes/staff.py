from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.routes.dependencies import get_session
from app.schemas.staff import StaffCreate, StaffResponse
from app.services.staff import (
    create_staff_item,
    delete_staff_item,
    get_staff,
    list_staff,
    update_staff_item,
)

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(payload: StaffCreate, session: Session = Depends(get_session)):
    return create_staff_item(session, payload)


@router.get("/", response_model=List[StaffResponse])
def read_staffs(session: Session = Depends(get_session)):
    return list_staff(session)


@router.get("/{item_id}", response_model=StaffResponse)
def read_staff(item_id: str, session: Session = Depends(get_session)):
    item = get_staff(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=StaffResponse)
def update_staff(item_id: str, payload: StaffCreate, session: Session = Depends(get_session)):
    item = update_staff_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_staff_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
