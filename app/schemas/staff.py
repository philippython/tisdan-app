from pydantic import BaseModel


class StaffCreate(BaseModel):
    department: str
    user_id: str


class StaffResponse(BaseModel):
    id: str
    department: str
    user_id: str

    class Config:
        orm_mode = True
