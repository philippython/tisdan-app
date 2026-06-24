from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class BroadcastGeneralCreate(BaseModel):
    title: str
    message: str


class BroadcastGeneralResponse(BaseModel):
    id: UUID
    title: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BroadcastPersonalCreate(BaseModel):
    user_id: UUID
    message: str


class BroadcastPersonalResponse(BaseModel):
    id: UUID
    user_id: UUID
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}
