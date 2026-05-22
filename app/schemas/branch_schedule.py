from pydantic import BaseModel
from datetime import time


class BranchScheduleCreate(BaseModel):
    day: str
    opening_time: time
    closing_time: time
    branch_id: str


class BranchScheduleResponse(BaseModel):
    id: str
    day: str
    opening_time: time
    closing_time: time
    branch_id: str

    class Config:
        orm_mode = True
