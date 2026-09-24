from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class ReferralCreate(BaseModel):
    coordinator_id: Optional[UUID] = None
    coordinator_code: Optional[str] = None
    patient_name: str
    patient_phone: str
    test_name: Optional[str] = None
    branch_name: Optional[str] = None
    commission: Optional[str] = None
    status: Optional[str] = "registered"


class ReferralResponse(BaseModel):
    id: UUID
    coordinator_id: UUID
    patient_name: str
    patient_phone: str
    test_name: Optional[str] = None
    branch_name: Optional[str] = None
    commission: Optional[str] = None
    status: str
    created_at: datetime
    coordinator_code: Optional[str] = None
    coordinator_name: Optional[str] = None

    model_config = {"from_attributes": True}


class ReferralUpdate(BaseModel):
    coordinator_id: Optional[UUID] = None
    coordinator_code: Optional[str] = None
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None
    test_name: Optional[str] = None
    branch_name: Optional[str] = None
    commission: Optional[str] = None
    status: Optional[str] = None
