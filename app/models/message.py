import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    chat_id: uuid.UUID = Field(
        foreign_key="chats.id"
    )

    sender_id: uuid.UUID = Field(
        index=True
    )

    sender_role: str  # DOCTOR or CLIENT

    content: str

    is_read: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    chat: Optional["Chat"] = Relationship(
        back_populates="messages"
    )