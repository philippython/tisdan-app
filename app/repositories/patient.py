from typing import Any, Dict
from sqlmodel import Session
from app.models import Patient
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_patients(session: Session):
    return get_all_items(session, Patient)


def get_patient_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Patient, item_id)


def create_patient(session: Session, data: Dict[str, Any]):
    return create_item(session, Patient, data)


def update_patient(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Patient, item_id, data)


def delete_patient(session: Session, item_id: Any):
    return delete_item(session, Patient, item_id)
