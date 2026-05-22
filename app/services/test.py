from typing import Any
from sqlmodel import Session
from repositories.test import (
    create_test,
    delete_test,
    get_test_by_id,
    get_all_test,
    update_test,
)


def list_test(session: Session):
    return get_all_test(session)


def get_test(session: Session, item_id: Any):
    return get_test_by_id(session, item_id)


def create_test_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_test(session, data)


def update_test_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_test(session, item_id, data)


def delete_test_item(session: Session, item_id: Any):
    return delete_test(session, item_id)
