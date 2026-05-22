from pydantic import BaseModel


class BranchCreate(BaseModel):
    name: str
    address: str
    branch_code: str


class BranchResponse(BaseModel):
    id: str
    name: str
    address: str
    branch_code: str

    class Config:
        orm_mode = True
