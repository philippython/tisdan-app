from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.enums.booking_status_enum import BookingStatus

class BookingCreate(BaseModel):
    booking_date: datetime
    user_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
    test_id: UUID
    branch_id: UUID

    @model_validator(mode="after")
    def require_user_or_customer(self):
        if not self.user_id and not self.customer_id:
            raise ValueError("Either user_id or customer_id must be provided")
        return self


class BookingResponse(BaseModel):
    id: UUID
    booking_date: datetime
    status: BookingStatus
    user_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
    test_id: UUID
    branch_id: UUID
    user_full_name: Optional[str] = None
    customer_full_name: Optional[str] = None
    test_name: Optional[str] = None
    branch_name: Optional[str] = None

    model_config = {"from_attributes": True}
