from pydantic import BaseModel
from datetime import datetime
from app.enums.result_status_enum import ResultStatus


class ResultCreate(BaseModel):
    booking_id: str
    result_text: str


class ResultResponse(BaseModel):
    id: str
    booking_id: str
    result_text: str
    status: ResultStatus
    uploaded_at: datetime

    class Config:
        orm_mode = True
