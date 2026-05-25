from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class ChatCreate(BaseModel):
    doctor_id: UUID
    client_id: UUID


class ChatResponse(BaseModel):
    id: UUID
    doctor_id: UUID
    client_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
