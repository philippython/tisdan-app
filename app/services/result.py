from typing import Any
from sqlmodel import Session
from app.repositories.result import (
    create_result,
    delete_result,
    get_result_by_id,
    get_all_result,
    update_result,
)


def list_result(session: Session):
    return get_all_result(session)


def get_result(session: Session, item_id: Any):
    return get_result_by_id(session, item_id)


def create_result_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_result(session, data)


def update_result_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_result(session, item_id, data)


def delete_result_item(session: Session, item_id: Any):
    return delete_result(session, item_id)
