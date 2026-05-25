from pydantic import BaseModel
from uuid import UUID


class StaffCreate(BaseModel):
    department: str
    user_id: UUID


class StaffResponse(BaseModel):
    id: UUID
    department: str
    user_id: UUID

    model_config = {"from_attributes": True}
