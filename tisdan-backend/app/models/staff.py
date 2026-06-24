import uuid

from sqlmodel import SQLModel, Field


class Staff(SQLModel, table=True):
    __tablename__ = "staff"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    department: str

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        unique=True
    )