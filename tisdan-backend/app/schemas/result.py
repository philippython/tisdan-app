from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.enums.result_status_enum import ResultStatus


class ResultCreate(BaseModel):
    booking_id: UUID
    result_text: str
    # RELEASED sends the result to the patient on WhatsApp straight away;
    # PENDING keeps it internal until someone releases it.
    status: Optional[ResultStatus] = None


class ResultUpdate(BaseModel):
    booking_id: Optional[UUID] = None
    result_text: Optional[str] = None
    status: Optional[ResultStatus] = None


class ResultResponse(BaseModel):
    id: UUID
    booking_id: UUID
    result_text: str
    status: ResultStatus
    uploaded_at: datetime
    patient_name: Optional[str] = None
    test_name: Optional[str] = None
    branch_name: Optional[str] = None
    booking_date: Optional[datetime] = None

    model_config = {"from_attributes": True}
