from pydantic import BaseModel
from datetime import datetime


class BookingCreate(BaseModel):
    booking_date: datetime
    user_id: str
    test_id: str
    branch_id: str