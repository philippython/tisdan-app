from typing import Any
from sqlmodel import Session, select
from app.repositories.branch import (
    create_branch,
    delete_branch,
    get_branch_by_id,
    get_all_branch,
    update_branch,
)
from app.repositories.branch_schedule import (
    create_branch_schedule,
    update_branch_schedule,
)
from app.utils.bot_notify import send_whatsapp_via_bot, format_phone
from app.models import BranchSchedule, Customer, User


def _get_branch_schedule(session: Session, branch_id: Any):
    statement = select(BranchSchedule).where(BranchSchedule.branch_id == branch_id)
    return session.exec(statement).first()


def _attach_schedule_fields(session: Session, item: Any):
    if item is None:
        return item
    # Return a plain dict combining branch fields with an attached schedule
    result = item.dict() if hasattr(item, "dict") else dict(item.__dict__)

    schedule = _get_branch_schedule(session, item.id)
    if schedule:
        result["schedule_day"] = schedule.day
        result["schedule_opening_time"] = schedule.opening_time
        result["schedule_closing_time"] = schedule.closing_time
    else:
        result["schedule_day"] = None
        result["schedule_opening_time"] = None
        result["schedule_closing_time"] = None

    return result


def list_branch(session: Session):
    items = get_all_branch(session)
    return [_attach_schedule_fields(session, item) for item in items]


def get_branch(session: Session, item_id: Any):
    item = get_branch_by_id(session, item_id)
    return _attach_schedule_fields(session, item)


def _ensure_schedule_for_branch(session: Session, branch_id: Any, data: dict[str, Any]):
    day = data.get("schedule_day")
    opening_time = data.get("schedule_opening_time")
    closing_time = data.get("schedule_closing_time")
    if not (day and opening_time and closing_time):
        return

    existing = _get_branch_schedule(session, branch_id)
    if existing:
        update_branch_schedule(session, existing.id, {
            "day": day,
            "opening_time": opening_time,
            "closing_time": closing_time,
        })
    else:
        create_branch_schedule(session, {
            "branch_id": branch_id,
            "day": day,
            "opening_time": opening_time,
            "closing_time": closing_time,
        })


def create_branch_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    item = create_branch(session, data)

    if item is not None:
        _ensure_schedule_for_branch(session, item.id, data)
        _attach_schedule_fields(session, item)

    # notify customers/users about new branch
    try:
        name = data.get("name", "New Branch")
        address = data.get("address", "Address available on site")
        body = f"📍 *New Branch Opened*\n\n{name}\n{address}\n\nVisit us today — Tisdan Care"

        stmt = select(Customer).where(Customer.phone_number != None)
        for cust in session.exec(stmt):
            to = format_phone(cust.phone_number)
            if to:
                send_whatsapp_via_bot(to, body)

        stmt2 = select(User).where(User.role == "CLIENT")
        for u in session.exec(stmt2):
            to = format_phone(u.phone_number)
            if to:
                send_whatsapp_via_bot(to, body)
    except Exception:
        pass

    return item


def update_branch_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    item = update_branch(session, item_id, data)
    if item is not None:
        _ensure_schedule_for_branch(session, item.id, data)
        _attach_schedule_fields(session, item)
    return item


def delete_branch_item(session: Session, item_id: Any):
    return delete_branch(session, item_id)
