from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class MessageCreate(BaseModel):
    chat_id: UUID
    sender_id: UUID
    sender_role: str
    content: str


class MessageResponse(BaseModel):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    sender_role: str
    content: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
