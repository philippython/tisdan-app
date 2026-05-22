from pydantic import BaseModel


class ClientCreate(BaseModel):
    gender: str
    age: int
    user_id: str


class ClientResponse(BaseModel):
    id: str
    gender: str
    age: int
    user_id: str

    class Config:
        orm_mode = True
