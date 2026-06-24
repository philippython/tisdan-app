import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from app.enums.booking_status_enum import BookingStatus


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    booking_date: datetime

    status: BookingStatus = Field(
        default=BookingStatus.PENDING
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id"
    )

    test_id: uuid.UUID = Field(
        foreign_key="tests.id"
    )

    branch_id: uuid.UUID = Field(
        foreign_key="branches.id"
    )

    customer_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="customers.id",
    )

    user: Optional["User"] = Relationship(
        back_populates="bookings"
    )

    customer: Optional["Customer"] = Relationship(
        back_populates="bookings"
    )