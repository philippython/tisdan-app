"""Phone-number lookups for WhatsApp notifications."""
from typing import Any, List, Optional

from sqlmodel import Session, select

from app.enums.role_enum import UserRole
from app.models import Booking, Customer, User


def booking_patient(session: Session, booking: Optional[Booking]) -> tuple[Optional[str], Optional[str]]:
    """(name, phone) of whoever the booking is for — a customer (WhatsApp
    bookings) or a registered user (portal bookings)."""
    if booking is None:
        return None, None
    if booking.customer_id:
        customer = session.get(Customer, booking.customer_id)
        if customer:
            return customer.full_name, customer.phone_number
    if booking.user_id:
        user = session.get(User, booking.user_id)
        if user:
            return user.full_name, user.phone_number
    return None, None


def booking_patient_phones(session: Session, booking_id: Any) -> List[str]:
    booking = session.get(Booking, booking_id) if booking_id else None
    _, phone = booking_patient(session, booking)
    return [phone] if phone else []


def staff_phones(session: Session) -> List[str]:
    stmt = select(User).where(User.role.in_([UserRole.ADMIN, UserRole.STAFF]))
    return [u.phone_number for u in session.exec(stmt) if u.phone_number]


def client_phones(session: Session) -> List[str]:
    """Everyone who should receive general announcements."""
    phones = [
        c.phone_number
        for c in session.exec(select(Customer).where(Customer.phone_number != None))  # noqa: E711
    ]
    phones += [
        u.phone_number
        for u in session.exec(select(User).where(User.role == UserRole.CLIENT))
        if u.phone_number
    ]
    return phones
