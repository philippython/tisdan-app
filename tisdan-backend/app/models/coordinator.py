import uuid
from typing import List

from sqlmodel import SQLModel, Field, Relationship


class Coordinator(SQLModel, table=True):
    __tablename__ = "coordinators"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    referral_code: str = Field(
        unique=True,
        index=True
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        unique=True
    )

    referrals: List["Referral"] = Relationship(
        back_populates="coordinator"
    )
