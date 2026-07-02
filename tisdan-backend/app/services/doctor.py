from typing import Any
from sqlmodel import Session
from app.models import User
from app.repositories.doctor import (
    create_doctor,
    delete_doctor,
    get_doctor_by_id,
    get_all_doctor,
    update_doctor,
)


def _enrich_doctor(session: Session, item):
    if item is None:
        return item

    result = item.dict()
    if getattr(item, "user_id", None):
        user = session.get(User, item.user_id)
        if user and getattr(user, "full_name", None):
            result["user_full_name"] = user.full_name

    return result


def list_doctor(session: Session):
    return [_enrich_doctor(session, item) for item in get_all_doctor(session)]


def get_doctor(session: Session, item_id: Any):
    return _enrich_doctor(session, get_doctor_by_id(session, item_id))


def create_doctor_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_doctor(session, data)


def update_doctor_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_doctor(session, item_id, data)


def delete_doctor_item(session: Session, item_id: Any):
    return delete_doctor(session, item_id)
