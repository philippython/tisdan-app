from pydantic import BaseModel


class TestCreate(BaseModel):
    name: str
    description: str
    price: float