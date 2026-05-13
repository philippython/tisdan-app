from pydantic import BaseModel


class ResultCreate(BaseModel):
    booking_id: str
    result_text: str