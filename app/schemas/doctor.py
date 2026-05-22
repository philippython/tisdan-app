from pydantic import BaseModel


class DoctorCreate(BaseModel):
    specialization: str
    license_number: str
    user_id: str


class DoctorResponse(BaseModel):
    id: str
    specialization: str
    license_number: str
    user_id: str

    class Config:
        orm_mode = True
