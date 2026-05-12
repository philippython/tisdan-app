import uuid
from typing import List

from sqlmodel import SQLModel, Field, Relationship


class Branch(SQLModel, table=True):
    __tablename__ = "branches"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    name: str = Field(
        max_length=255
    )

    address: str = Field(
        max_length=255
    )

    branch_code: str = Field(
        unique=True,
        index=True
    )

    users: List["User"] = Relationship(
        back_populates="branch"
    )

    schedules: List["BranchSchedule"] = Relationship(
        back_populates="branch"
    )