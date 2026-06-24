from typing import Any
from sqlmodel import Session
from app.repositories.patient import (
    create_patient,
    delete_patient,
    get_patient_by_id,
    get_all_patients,
    update_patient,
)


def list_patients(session: Session):
    return get_all_patients(session)


def get_patient(session: Session, item_id: Any):
    return get_patient_by_id(session, item_id)


def create_patient_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_patient(session, data)


def update_patient_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_patient(session, item_id, data)


def delete_patient_item(session: Session, item_id: Any):
    return delete_patient(session, item_id)
