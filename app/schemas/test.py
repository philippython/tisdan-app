from pydantic import BaseModel


class TestCreate(BaseModel):
    name: str
    description: str
    price: float


class TestResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True
