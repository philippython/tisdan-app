import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field


class BroadcastPersonal(SQLModel, table=True):
    __tablename__ = "broadcast_personal"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id"
    )

    message: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )