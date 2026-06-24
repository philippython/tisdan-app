from typing import Any, Dict
from sqlmodel import Session
from app.models import Booking
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_booking(session: Session):
    return get_all_items(session, Booking)


def get_booking_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Booking, item_id)


def create_booking(session: Session, data: Dict[str, Any]):
    return create_item(session, Booking, data)


def update_booking(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Booking, item_id, data)


def delete_booking(session: Session, item_id: Any):
    return delete_item(session, Booking, item_id)
