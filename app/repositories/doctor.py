from typing import Any, Dict
from sqlmodel import Session
from models import Doctor
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_doctor(session: Session):
    return get_all_items(session, Doctor)


def get_doctor_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Doctor, item_id)


def create_doctor(session: Session, data: Dict[str, Any]):
    return create_item(session, Doctor, data)


def update_doctor(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Doctor, item_id, data)


def delete_doctor(session: Session, item_id: Any):
    return delete_item(session, Doctor, item_id)
