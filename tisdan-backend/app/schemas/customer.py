from pydantic import BaseModel
from uuid import UUID


class CustomerCreate(BaseModel):
    full_name: str
    phone_number: str | None = None
    address: str | None = None


class CustomerResponse(BaseModel):
    id: UUID
    full_name: str
    phone_number: str | None = None
    address: str | None = None

    model_config = {"from_attributes": True}


class CustomerUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    address: str | None = None
