from pydantic import BaseModel


class BroadcastGeneralCreate(BaseModel):
    title: str
    message: str


class BroadcastPersonalCreate(BaseModel):
    user_id: str
    message: str