from pydantic import BaseModel
from uuid import UUID


class TestCreate(BaseModel):
    name: str
    description: str
    price: float


class TestResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float

    model_config = {"from_attributes": True}
