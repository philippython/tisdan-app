from typing import Any
from sqlmodel import Session
from repositories.doctor import (
    create_doctor,
    delete_doctor,
    get_doctor_by_id,
    get_all_doctor,
    update_doctor,
)


def list_doctor(session: Session):
    return get_all_doctor(session)


def get_doctor(session: Session, item_id: Any):
    return get_doctor_by_id(session, item_id)


def create_doctor_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_doctor(session, data)


def update_doctor_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_doctor(session, item_id, data)


def delete_doctor_item(session: Session, item_id: Any):
    return delete_doctor(session, item_id)
