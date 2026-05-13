from pydantic import BaseModel


class ClientCreate(BaseModel):
    gender: str
    age: int
    user_id: str