from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.services.doctor import (
    create_doctor_item,
    delete_doctor_item,
    get_doctor,
    list_doctor,
    update_doctor_item,
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN))):
    return create_doctor_item(session, payload)


@router.get("/", response_model=List[DoctorResponse])
def read_doctors(session: Session = Depends(get_session)):
    return list_doctor(session)


@router.get("/{item_id}", response_model=DoctorResponse)
def read_doctor(item_id: str, session: Session = Depends(get_session)):
    item = get_doctor(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=DoctorResponse)
def update_doctor(item_id: str, payload: DoctorCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN))):
    item = update_doctor_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN))):
    deleted = delete_doctor_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
