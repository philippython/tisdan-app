from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class ChatCreate(BaseModel):
    doctor_id: UUID
    customer_id: UUID


class ChatResponse(BaseModel):
    id: UUID
    doctor_id: UUID
    customer_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatUpdate(BaseModel):
    doctor_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
