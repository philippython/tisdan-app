import uuid
from datetime import time
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class BranchSchedule(SQLModel, table=True):
    __tablename__ = "branch_schedules"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    day: str

    opening_time: time

    closing_time: time

    branch_id: uuid.UUID = Field(
        foreign_key="branches.id"
    )

    branch: Optional["Branch"] = Relationship(
        back_populates="schedules"
    )