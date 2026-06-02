from typing import Any
from sqlmodel import Session
from app.core.security import get_password_hash, verify_password
from app.repositories.user import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_all_user,
    update_user,
)


def list_user(session: Session):
    return get_all_user(session)


def get_user(session: Session, item_id: Any):
    return get_user_by_id(session, item_id)


def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_user_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    if "password" in data:
        data["password"] = get_password_hash(data["password"])
    return create_user(session, data)


def update_user_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    if "password" in data:
        data["password"] = get_password_hash(data["password"])
    return update_user(session, item_id, data)


def delete_user_item(session: Session, item_id: Any):
    return delete_user(session, item_id)
