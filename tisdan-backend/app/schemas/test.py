from pydantic import BaseModel
from uuid import UUID


class TestCreate(BaseModel):
    name: str
    description: str
    price: float
    branch_id: UUID | None = None


class TestResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    branch_id: UUID | None = None

    model_config = {"from_attributes": True}
