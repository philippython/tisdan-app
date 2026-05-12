import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field

from enums.result_status_enum import ResultStatus


class Result(SQLModel, table=True):
    __tablename__ = "results"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    booking_id: uuid.UUID = Field(
        foreign_key="bookings.id"
    )

    result_text: str

    status: ResultStatus = Field(
        default=ResultStatus.PENDING
    )

    uploaded_at: datetime = Field(
        default_factory=datetime.utcnow
    )