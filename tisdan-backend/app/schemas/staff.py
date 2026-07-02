from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class StaffCreate(BaseModel):
    department: str
    user_id: UUID


class StaffResponse(BaseModel):
    id: UUID
    department: str
    user_id: UUID
    user_full_name: Optional[str] = None

    model_config = {"from_attributes": True}
