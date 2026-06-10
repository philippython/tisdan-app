from pydantic import BaseModel
from uuid import UUID


class PatientCreate(BaseModel):
    gender: str
    age: int
    user_id: UUID


class PatientResponse(BaseModel):
    id: UUID
    gender: str
    age: int
    user_id: UUID

    model_config = {"from_attributes": True}
