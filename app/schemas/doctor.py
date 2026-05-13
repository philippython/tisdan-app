from pydantic import BaseModel


class DoctorCreate(BaseModel):
    specialization: str
    license_number: str
    user_id: str