from pydantic import BaseModel
from datetime import time
from typing import Optional
from uuid import UUID


class BranchScheduleCreate(BaseModel):
    day: str
    opening_time: time
    closing_time: time
    branch_id: UUID


class BranchScheduleResponse(BaseModel):
    id: UUID
    day: str
    opening_time: time
    closing_time: time
    branch_id: UUID
    branch_name: Optional[str] = None

    model_config = {"from_attributes": True}


class BranchScheduleUpdate(BaseModel):
    day: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    branch_id: Optional[UUID] = None
