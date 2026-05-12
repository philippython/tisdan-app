import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enums.role_enum import UserRole


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    email: str = Field(
        unique=True,
        index=True,
        max_length=255
    )

    password: str = Field(
        max_length=255
    )

    full_name: str = Field(
        max_length=255
    )

    phone_number: str = Field(
        max_length=15
    )

    role: UserRole

    branch_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="branches.id"
    )

    branch: Optional["Branch"] = Relationship(
        back_populates="users"
    )

    bookings: List["Booking"] = Relationship(
        back_populates="user"
    )