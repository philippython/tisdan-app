import traceback
from typing import Any, Optional
from sqlmodel import Session
from app.repositories.result import (
    create_result,
    delete_result,
    get_result_by_id,
    get_all_result,
    update_result,
    get_results_by_customer_id,
    get_results_by_customer_name as _results_by_customer_name,
)
from app.utils.bot_notify import queue_whatsapp
from app.enums.result_status_enum import ResultStatus
from app.models import Booking, Branch, Result, Test
from app.schemas.result import ResultResponse
from app.services.recipients import booking_patient


def enrich_result(session: Session, item: Optional[Result]) -> Optional[ResultResponse]:
    if item is None:
        return None
    booking = session.get(Booking, item.booking_id) if item.booking_id else None
    patient_name, _ = booking_patient(session, booking)
    test = session.get(Test, booking.test_id) if booking else None
    branch = session.get(Branch, booking.branch_id) if booking else None
    return ResultResponse(
        id=item.id,
        booking_id=item.booking_id,
        result_text=item.result_text,
        status=item.status,
        uploaded_at=item.uploaded_at,
        patient_name=patient_name,
        test_name=test.name if test else None,
        branch_name=branch.name if branch else None,
        booking_date=booking.booking_date if booking else None,
    )


def _notify_result_released(session: Session, item: Result, updated: bool = False) -> None:
    try:
        enriched = enrich_result(session, item)
        booking = session.get(Booking, item.booking_id)
        _, phone = booking_patient(session, booking)
        heading = "🔔 *Result Updated*" if updated else "✅ *Result Available*"
        body = (
            f"{heading}\n\n"
            f"Patient: {enriched.patient_name or 'N/A'}\n"
            f"Test: {enriched.test_name or 'N/A'}\n"
            f"Result: {item.result_text}\n\n"
            f"Reference: {item.booking_id}\n"
            "Please contact your clinic for interpretation. — Tisdan Care"
        )
        queue_whatsapp([phone], body)
    except Exception:
        # Do not fail the primary operation if notifications fail,
        # but always log so failures are visible instead of silent.
        traceback.print_exc()


def list_result(session: Session):
    items = sorted(get_all_result(session), key=lambda r: r.uploaded_at, reverse=True)
    return [enrich_result(session, item) for item in items]


def get_result(session: Session, item_id: Any):
    return enrich_result(session, get_result_by_id(session, item_id))


def create_result_item(session: Session, payload: Any):
    data = payload.model_dump(exclude_none=True)
    item = create_result(session, data)
    if item.status == ResultStatus.RELEASED:
        _notify_result_released(session, item)
    return enrich_result(session, item)


def update_result_item(session: Session, item_id: Any, payload: Any):
    data = payload.model_dump(exclude_unset=True)
    existing = get_result_by_id(session, item_id)
    if existing is None:
        return None
    was_released = existing.status == ResultStatus.RELEASED
    old_text = existing.result_text

    item = update_result(session, item_id, data)
    if item.status == ResultStatus.RELEASED and (not was_released or item.result_text != old_text):
        _notify_result_released(session, item, updated=was_released)
    return enrich_result(session, item)


def delete_result_item(session: Session, item_id: Any):
    return delete_result(session, item_id)


def get_results_by_customer(session: Session, customer_id: Any):
    return [enrich_result(session, r) for r in get_results_by_customer_id(session, customer_id)]


def get_results_by_customer_name(session: Session, name: str):
    return [enrich_result(session, r) for r in _results_by_customer_name(session, name)]
