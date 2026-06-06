from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

from app.enums.role_enum import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    role: UserRole
    branch_id: Optional[UUID] = None


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    phone_number: str
    role: UserRole
    branch_id: Optional[UUID] = None

    model_config = {"from_attributes": True}
