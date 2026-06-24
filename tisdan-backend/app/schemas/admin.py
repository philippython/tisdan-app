from pydantic import BaseModel
from uuid import UUID


class AdminCreate(BaseModel):
    user_id: UUID


class AdminResponse(BaseModel):
    id: UUID
    user_id: UUID

    model_config = {"from_attributes": True}
