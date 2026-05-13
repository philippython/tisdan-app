from pydantic import BaseModel


class CoordinatorCreate(BaseModel):
    referral_code: str
    user_id: str