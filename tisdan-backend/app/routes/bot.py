"""Endpoints used only by the WhatsApp bot (authenticated with X-Bot-Key)."""
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from app.dependencies.authentication import require_bot
from app.enums.result_status_enum import ResultStatus
from app.models import Booking, Customer, Result, User
from app.routes.dependencies import get_session
from app.schemas.coordinator import CoordinatorResponse
from app.schemas.customer import CustomerResponse
from app.services.coordinator import get_coordinator_by_code
from app.services.result import enrich_result
from app.utils.bot_notify import format_phone

router = APIRouter(prefix="/bot", tags=["Bot"], dependencies=[Depends(require_bot)])


class BotCustomerRequest(BaseModel):
    full_name: str
    phone_number: str
    address: Optional[str] = None


class BotResult(BaseModel):
    reference: str
    patient_name: Optional[str] = None
    test_name: Optional[str] = None
    branch_name: Optional[str] = None
    date: Optional[str] = None
    result_text: str


class BotResultsResponse(BaseModel):
    results: List[BotResult]
    # bookings found for this person/reference whose result isn't released yet
    pending: int = 0


@router.get("/coordinators/{code}", response_model=CoordinatorResponse)
def bot_coordinator(code: str, session: Session = Depends(get_session)):
    item = get_coordinator_by_code(session, code.strip().upper())
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown coordinator code")
    return item


def _customers_by_phone(session: Session, phone: str) -> List[Customer]:
    target = format_phone(phone)
    return [c for c in session.exec(select(Customer)).all() if format_phone(c.phone_number) == target]


def _users_by_phone(session: Session, phone: str) -> List[User]:
    target = format_phone(phone)
    return [u for u in session.exec(select(User)).all() if format_phone(u.phone_number) == target]


@router.post("/customers/", response_model=CustomerResponse)
def bot_find_or_create_customer(payload: BotCustomerRequest, session: Session = Depends(get_session)):
    existing = _customers_by_phone(session, payload.phone_number)
    if existing:
        customer = existing[0]
        if payload.address and not customer.address:
            customer.address = payload.address
            session.add(customer)
            session.commit()
            session.refresh(customer)
        return customer

    customer = Customer(
        full_name=payload.full_name,
        phone_number=format_phone(payload.phone_number),
        address=payload.address,
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def _collect(session: Session, bookings: List[Booking]) -> BotResultsResponse:
    results: List[BotResult] = []
    pending = 0
    for booking in sorted(bookings, key=lambda b: b.booking_date, reverse=True):
        released = session.exec(
            select(Result).where(
                Result.booking_id == booking.id, Result.status == ResultStatus.RELEASED
            )
        ).all()
        if not released:
            pending += 1
        for r in released:
            e = enrich_result(session, r)
            results.append(
                BotResult(
                    reference=str(booking.id),
                    patient_name=e.patient_name,
                    test_name=e.test_name,
                    branch_name=e.branch_name,
                    date=booking.booking_date.strftime("%d %B %Y"),
                    result_text=r.result_text,
                )
            )
    return BotResultsResponse(results=results, pending=pending)


@router.get("/results", response_model=BotResultsResponse)
def bot_results(
    phone: Optional[str] = None,
    reference: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """Released results for a booking reference (booking or result id) or for
    every booking made by the owner of a phone number."""
    if reference:
        try:
            ref = uuid.UUID(reference.strip())
        except ValueError:
            return BotResultsResponse(results=[])
        booking = session.get(Booking, ref)
        if booking is None:
            result = session.get(Result, ref)
            booking = session.get(Booking, result.booking_id) if result else None
        return _collect(session, [booking] if booking else [])

    if phone:
        customer_ids = [c.id for c in _customers_by_phone(session, phone)]
        user_ids = [u.id for u in _users_by_phone(session, phone)]
        bookings = [
            b
            for b in session.exec(select(Booking)).all()
            if b.customer_id in customer_ids or b.user_id in user_ids
        ]
        return _collect(session, bookings)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide phone or reference")
