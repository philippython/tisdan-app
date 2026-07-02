from typing import Any
from sqlmodel import Session
from app.models import User
from app.repositories.patient import (
    create_patient,
    delete_patient,
    get_patient_by_id,
    get_all_patients,
    update_patient,
)
from app.schemas.patient import PatientResponse


def _enrich_patient(session: Session, item):
    if item is None:
        return None

    user_full_name = None
    if getattr(item, "user_id", None):
        user = session.get(User, item.user_id)
        if user and getattr(user, "full_name", None):
            user_full_name = user.full_name

    return PatientResponse(
        id=item.id,
        gender=item.gender,
        age=item.age,
        user_id=item.user_id,
        user_full_name=user_full_name,
    )


def list_patients(session: Session):
    return [_enrich_patient(session, item) for item in get_all_patients(session)]


def get_patient(session: Session, item_id: Any):
    return _enrich_patient(session, get_patient_by_id(session, item_id))


def create_patient_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_patient(session, data)
    return _enrich_patient(session, item)


def update_patient_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_patient(session, item_id, data)
    return _enrich_patient(session, item)


def delete_patient_item(session: Session, item_id: Any):
    return delete_patient(session, item_id)
