from fastapi import APIRouter, Form, Request

from .flows import process_incoming_message

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
