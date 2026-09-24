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
    referral_count: int = 0

    model_config = {"from_attributes": True}


class CoordinatorUpdate(BaseModel):
    referral_code: Optional[str] = None
    user_id: Optional[UUID] = None
