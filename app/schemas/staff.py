from pydantic import BaseModel


class StaffCreate(BaseModel):
    department: str
    user_id: str