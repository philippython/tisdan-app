import uuid

from sqlmodel import SQLModel, Field


class Admin(SQLModel, table=True):
    __tablename__ = "admins"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )


    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        unique=True
    )