from typing import Any
from sqlmodel import Session
from app.repositories.result import (
    create_result,
    delete_result,
    get_result_by_id,
    get_all_result,
    update_result,
    get_results_by_customer_id,
    get_results_by_customer_name,
)
from app.utils.bot_notify import send_whatsapp_via_bot, format_phone
from app.models import Booking, Customer, User

from sqlmodel import select


def list_result(session: Session):
    return get_all_result(session)


def get_result(session: Session, item_id: Any):
    return get_result_by_id(session, item_id)


def create_result_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_result(session, data)

    # attempt to notify patient via booking -> customer or user
    try:
        booking = session.get(Booking, item.booking_id)
        phones = []
        if booking:
            if booking.customer_id:
                cust = session.get(Customer, booking.customer_id)
                if cust and cust.phone_number:
                    phones.append(cust.phone_number)
            if booking.user_id:
                user = session.get(User, booking.user_id)
                if user and getattr(user, "phone_number", None):
                    phones.append(user.phone_number)

        body = (
            "✅ *Result Available*\n\n"
            f"Booking: {str(item.booking_id)}\n"
            f"Result: {getattr(item, 'result_text', '')}\n\n"
            "Please contact your clinic for interpretation. — Tisdan Care"
        )
        for p in set(phones):
            to = format_phone(p)
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def update_result_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_result(session, item_id, data)
    if item is None:
        return None

    # notify patient about updated result
    try:
        booking = session.get(Booking, item.booking_id)
        phones = []
        if booking:
            if booking.customer_id:
                cust = session.get(Customer, booking.customer_id)
                if cust and cust.phone_number:
                    phones.append(cust.phone_number)
            if booking.user_id:
                user = session.get(User, booking.user_id)
                if user and getattr(user, "phone_number", None):
                    phones.append(user.phone_number)

        body = (
            "🔔 *Result Updated*\n\n"
            f"Booking: {str(item.booking_id)}\n"
            f"Result: {getattr(item, 'result_text', '')}\n\n"
            "Please check the updated report or contact your clinic. — Tisdan Care"
        )
        for p in set(phones):
            to = format_phone(p)
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def delete_result_item(session: Session, item_id: Any):
    return delete_result(session, item_id)


def get_results_by_customer(session: Session, customer_id: Any):
    return get_results_by_customer_id(session, customer_id)


def get_results_by_customer_name(session: Session, name: str):
    return get_results_by_customer_name(session, name)
