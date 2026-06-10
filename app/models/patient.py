import uuid

from sqlmodel import SQLModel, Field


class Patient(SQLModel, table=True):
    __tablename__ = "patients"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    gender: str

    age: int

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        unique=True
    )
