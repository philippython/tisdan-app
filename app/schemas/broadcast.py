from pydantic import BaseModel
from datetime import datetime


class BroadcastGeneralCreate(BaseModel):
    title: str
    message: str


class BroadcastGeneralResponse(BaseModel):
    id: str
    title: str
    message: str
    created_at: datetime

    class Config:
        orm_mode = True


class BroadcastPersonalCreate(BaseModel):
    user_id: str
    message: str


class BroadcastPersonalResponse(BaseModel):
    id: str
    user_id: str
    message: str
    created_at: datetime

    class Config:
        orm_mode = True
