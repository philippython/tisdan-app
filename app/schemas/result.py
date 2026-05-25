from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.enums.result_status_enum import ResultStatus


class ResultCreate(BaseModel):
    booking_id: UUID
    result_text: str


class ResultResponse(BaseModel):
    id: UUID
    booking_id: UUID
    result_text: str
    status: ResultStatus
    uploaded_at: datetime

    model_config = {"from_attributes": True}
