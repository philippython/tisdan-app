from pydantic import BaseModel
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

    model_config = {"from_attributes": True}
