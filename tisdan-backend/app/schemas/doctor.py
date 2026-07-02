from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class DoctorCreate(BaseModel):
    specialization: str
    license_number: str
    user_id: UUID


class DoctorResponse(BaseModel):
    id: UUID
    specialization: str
    license_number: str
    user_id: UUID
    user_full_name: Optional[str] = None

    model_config = {"from_attributes": True}
