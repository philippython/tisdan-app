from pydantic import BaseModel, EmailStr
from typing import Optional

from enums.role_enum import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    role: UserRole
    branch_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    phone_number: str
    role: UserRole
    branch_id: Optional[str] = None

    class Config:
        orm_mode = True
