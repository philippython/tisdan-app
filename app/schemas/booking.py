from pydantic import BaseModel
from datetime import datetime
from app.enums.booking_status_enum import BookingStatus


class BookingCreate(BaseModel):
    booking_date: datetime
    user_id: str
    test_id: str
    branch_id: str


class BookingResponse(BaseModel):
    id: str
    booking_date: datetime
    status: BookingStatus
    user_id: str
    test_id: str
    branch_id: str

    class Config:
        orm_mode = True
