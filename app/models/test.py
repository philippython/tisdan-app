import uuid
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Test(SQLModel, table=True):
    __tablename__ = "tests"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    name: str = Field(
        max_length=255
    )

    description: str

    price: float

    branch_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="branches.id",
    )

    branch: Optional["Branch"] = Relationship(
        back_populates="tests"
    )