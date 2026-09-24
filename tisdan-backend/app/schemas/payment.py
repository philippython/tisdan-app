from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.enums.payment_for_enum import PaymentFor
from app.enums.payment_status_enum import PaymentStatus


class PaymentCreate(BaseModel):
    amount: float
    currency: Optional[str] = "NGN"
    payer_id: UUID
    payment_for: PaymentFor
    booking_id: Optional[UUID] = None
    coordinator_id: Optional[UUID] = None
    reference: Optional[str] = None
    status: Optional[PaymentStatus] = None


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    payment_for: Optional[PaymentFor] = None
    booking_id: Optional[UUID] = None
    coordinator_id: Optional[UUID] = None
    reference: Optional[str] = None
    status: Optional[PaymentStatus] = None


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
    payer_name: Optional[str] = None

    model_config = {"from_attributes": True}


class PaymentInitializeRequest(BaseModel):
    booking_id: Optional[UUID] = None
    payer_id: UUID
    amount: float
    currency: Optional[str] = "NGN"
    payment_for: Optional[PaymentFor] = PaymentFor.TEST


class PaymentInitializeResponse(BaseModel):
    payment: PaymentResponse
    authorization_url: Optional[str] = None
    access_code: Optional[str] = None
    reference: str
    whatsapp_sent: bool = False
