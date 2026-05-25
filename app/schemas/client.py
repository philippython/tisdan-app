from pydantic import BaseModel
from uuid import UUID


class ClientCreate(BaseModel):
    gender: str
    age: int
    user_id: str


class ClientResponse(BaseModel):
    id: UUID
    gender: str
    age: int
    user_id: UUID

    model_config = {"from_attributes": True}
