import uuid

from sqlmodel import SQLModel, Field


class Doctor(SQLModel, table=True):
    __tablename__ = "doctors"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    specialization: str

    license_number: str

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        unique=True
    )