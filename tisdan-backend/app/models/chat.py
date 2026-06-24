import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


class Chat(SQLModel, table=True):
    __tablename__ = "chats"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    doctor_id: uuid.UUID = Field(
        foreign_key="doctors.id"
    )

    customer_id: uuid.UUID = Field(
        foreign_key="customers.id"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    messages: List["Message"] = Relationship(
        back_populates="chat"
    )