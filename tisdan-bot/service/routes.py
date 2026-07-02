from fastapi import APIRouter, Form, Request

from .flows import process_incoming_message
from fastapi import Body
from .twilio_client import send_whatsapp_message

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "ok", "message": "FastAPI + Twilio webhook is ready."}


@router.post("/sms")
async def sms_reply(
    request: Request,
    Body: str = Form(""),
    From: str = Form(""),
    To: str = Form(""),
):
    return await process_incoming_message(From, Body)



@router.post("/send")
async def send_message(
    to: str = Body(..., embed=True),
    body: str = Body(..., embed=True),
):
    """Internal endpoint used by backend to send WhatsApp messages."""
    ok = send_whatsapp_message(to, body)
    return {"ok": ok}
