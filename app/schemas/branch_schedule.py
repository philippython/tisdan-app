from pydantic import BaseModel
from datetime import time


class BranchScheduleCreate(BaseModel):
    day: str
    opening_time: time
    closing_time: time
    branch_id: str