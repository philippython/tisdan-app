import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field


class BroadcastGeneral(SQLModel, table=True):
    __tablename__ = "broadcast_general"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    title: str

    message: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )