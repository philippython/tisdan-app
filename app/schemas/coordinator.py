from pydantic import BaseModel


class CoordinatorCreate(BaseModel):
    referral_code: str
    user_id: str


class CoordinatorResponse(BaseModel):
    id: str
    referral_code: str
    user_id: str

    class Config:
        orm_mode = True
