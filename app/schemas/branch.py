from pydantic import BaseModel
from uuid import UUID


class BranchCreate(BaseModel):
    name: str
    address: str
    branch_code: str


class BranchResponse(BaseModel):
    id: UUID
    name: str
    address: str
    branch_code: str
    model_config = {"from_attributes": True}
