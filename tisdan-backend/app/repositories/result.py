from typing import Any, Dict
from sqlmodel import Session
from app.models import Result
from app.repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item
from app.models import Booking, Customer
from sqlmodel import select


def get_all_result(session: Session):
    return get_all_items(session, Result)


def get_result_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, Result, item_id)


def create_result(session: Session, data: Dict[str, Any]):
    return create_item(session, Result, data)


def update_result(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, Result, item_id, data)


def delete_result(session: Session, item_id: Any):
    return delete_item(session, Result, item_id)


def get_results_by_customer_id(session: Session, customer_id: Any):
    statement = select(Result).join(Booking, Result.booking_id == Booking.id).where(Booking.customer_id == customer_id)
    return session.exec(statement).all()


def get_results_by_customer_name(session: Session, name: str):
    # join Result -> Booking -> Customer and filter by customer full_name
    statement = (
        select(Result)
        .join(Booking, Result.booking_id == Booking.id)
        .join(Customer, Booking.customer_id == Customer.id)
        .where(Customer.full_name.ilike(f"%{name}%"))
    )
    return session.exec(statement).all()
