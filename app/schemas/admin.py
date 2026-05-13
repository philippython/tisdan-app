from pydantic import BaseModel


class AdminCreate(BaseModel):
    access_level: str
    user_id: str