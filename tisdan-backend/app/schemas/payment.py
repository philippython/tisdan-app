from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.enums.payment_for_enum import PaymentFor
from app.enums.payment_status_enum import PaymentStatus


class PaymentCreate(BaseModel):
    amount: float
    currency: Optional[str] = "USD"
    payer_id: UUID
    payment_for: PaymentFor
    booking_id: Optional[UUID] = None
    coordinator_id: Optional[UUID] = None
    reference: Optional[str] = None


class PaymentResponse(BaseModel):
    id: UUID
    amount: float
    currency: str
    payer_id: UUID
    payment_for: PaymentFor
    booking_id: Optional[UUID]
    coordinator_id: Optional[UUID]
    status: PaymentStatus
    reference: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
