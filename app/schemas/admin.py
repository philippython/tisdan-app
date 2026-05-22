from pydantic import BaseModel


class AdminCreate(BaseModel):
    user_id: str


class AdminResponse(BaseModel):
    id: str
    user_id: str

    class Config:
        orm_mode = True
