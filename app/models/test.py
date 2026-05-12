import uuid
from sqlmodel import SQLModel, Field


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