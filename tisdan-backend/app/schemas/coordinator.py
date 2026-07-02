from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class CoordinatorCreate(BaseModel):
    referral_code: str
    user_id: UUID


class CoordinatorResponse(BaseModel):
    id: UUID
    referral_code: str
    user_id: UUID
    user_full_name: Optional[str] = None

    model_config = {"from_attributes": True}
