from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatCreate(BaseModel):
    doctor_id: str
    client_id: str


class ChatResponse(BaseModel):
    id: str
    doctor_id: str
    client_id: str
    created_at: datetime