from pydantic import BaseModel
from datetime import time
from typing import Optional
from uuid import UUID


class BranchCreate(BaseModel):
    name: str
    address: str
    branch_code: str
    schedule_day: Optional[str] = None
    schedule_opening_time: Optional[time] = None
    schedule_closing_time: Optional[time] = None


class BranchResponse(BaseModel):
    id: UUID
    name: str
    address: str
    branch_code: str
    schedule_day: Optional[str] = None
    schedule_opening_time: Optional[time] = None
    schedule_closing_time: Optional[time] = None

    model_config = {"from_attributes": True}


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    branch_code: Optional[str] = None
    schedule_day: Optional[str] = None
    schedule_opening_time: Optional[time] = None
    schedule_closing_time: Optional[time] = None
