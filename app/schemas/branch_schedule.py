from pydantic import BaseModel
from datetime import time
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

    model_config = {"from_attributes": True}
