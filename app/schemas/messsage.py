from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    chat_id: str
    sender_id: str
    sender_role: str
    content: str


class MessageResponse(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    sender_role: str
    content: str
    is_read: bool
    created_at: datetime