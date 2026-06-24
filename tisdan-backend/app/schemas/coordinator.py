from pydantic import BaseModel
from uuid import UUID


class CoordinatorCreate(BaseModel):
    referral_code: str
    user_id: UUID


class CoordinatorResponse(BaseModel):
    id: UUID
    referral_code: str
    user_id: UUID

    model_config = {"from_attributes": True}
