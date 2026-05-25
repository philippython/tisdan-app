from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.enums.booking_status_enum import BookingStatus


class BookingCreate(BaseModel):
    booking_date: datetime
    user_id: UUID
    test_id: UUID
    branch_id: UUID


class BookingResponse(BaseModel):
    id: UUID
    booking_date: datetime
    status: BookingStatus
    user_id: UUID
    test_id: UUID
    branch_id: UUID

    model_config = {"from_attributes": True}
