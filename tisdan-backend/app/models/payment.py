import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

from app.enums.payment_for_enum import PaymentFor
from app.enums.payment_status_enum import PaymentStatus


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    amount: float

    currency: str = Field(default="USD")

    payer_id: uuid.UUID = Field(
        foreign_key="users.id"
    )

    payment_for: PaymentFor = Field(
        default=PaymentFor.TEST
    )

    booking_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="bookings.id"
    )

    coordinator_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="coordinators.id"
    )

    status: PaymentStatus = Field(
        default=PaymentStatus.PENDING
    )

    reference: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
