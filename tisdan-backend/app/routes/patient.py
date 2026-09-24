from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.services.patient import (
    create_patient_item,
    delete_patient_item,
    get_patient,
    list_patients,
    update_patient_item,
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    return create_patient_item(session, payload)


@router.get("/", response_model=List[PatientResponse])
def read_patients(session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF, UserRole.DOCTOR))):
    return list_patients(session)


@router.get("/{item_id}", response_model=PatientResponse)
def read_patient(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF, UserRole.DOCTOR))):
    item = get_patient(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=PatientResponse)
def update_patient(item_id: str, payload: PatientUpdate, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    item = update_patient_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    deleted = delete_patient_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
