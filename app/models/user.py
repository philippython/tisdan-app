import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, max_length=255)
    password: str = Field(index=True)
    full_name: str = Field(max_length=255)
    phone_number: str = Field(max_length=13)
    branch_code: str | None = Field(default=None)
    role: str 

