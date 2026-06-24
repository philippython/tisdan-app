import uuid
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    full_name: str = Field(
        max_length=255
    )

    phone_number: Optional[str] = Field(
        default=None,
        max_length=15
    )

    address: Optional[str] = Field(
        default=None,
        max_length=255
    )

    bookings: list["Booking"] = Relationship(back_populates="customer")
