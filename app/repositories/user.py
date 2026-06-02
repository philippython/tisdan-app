from typing import Any, Dict
from sqlmodel import Session, select
from app.models import User
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_user(session: Session):
    return get_all_items(session, User)


def get_user_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, User, item_id)


def get_user_by_email(session: Session, email: str):
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(session: Session, data: Dict[str, Any]):
    return create_item(session, User, data)


def update_user(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, User, item_id, data)


def delete_user(session: Session, item_id: Any):
    return delete_item(session, User, item_id)
