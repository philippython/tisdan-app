from pydantic import BaseModel
from typing import Optional
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
    user_full_name: Optional[str] = None

    model_config = {"from_attributes": True}
