import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Referral(SQLModel, table=True):
    __tablename__ = "referrals"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    coordinator_id: uuid.UUID = Field(
        foreign_key="coordinators.id"
    )

    patient_name: str

    patient_phone: str

    test_name: Optional[str] = None

    branch_name: Optional[str] = None

    commission: Optional[str] = None

    status: str = Field(
        default="registered"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    coordinator: Optional["Coordinator"] = Relationship(
        back_populates="referrals"
    )
