from pydantic import BaseModel


class BranchCreate(BaseModel):
    name: str
    address: str
    branch_code: str