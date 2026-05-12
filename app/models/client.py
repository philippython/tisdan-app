import uuid

from sqlmodel import SQLModel, Field


class Client(SQLModel, table=True):
    __tablename__ = "clients"

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