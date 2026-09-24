import logging
import os
import secrets

from fastapi import APIRouter, Body, Form, Header, HTTPException, Request
from twilio.request_validator import RequestValidator

from .flows import process_incoming_message
from .twilio_client import TWILIO_AUTH_TOKEN, send_whatsapp_message

logger = logging.getLogger("tisdan.bot")

router = APIRouter()

BOT_API_KEY = os.getenv("BOT_API_KEY", "")
# Public URL Twilio posts to (e.g. https://bot.example.com/sms). When set,
# incoming webhooks must carry a valid Twilio signature.
TWILIO_WEBHOOK_URL = os.getenv("TWILIO_WEBHOOK_URL", "")


@router.get("/")
async def root():
    return {"status": "ok", "message": "FastAPI + Twilio webhook is ready."}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/sms")
async def sms_reply(
    request: Request,
    Body: str = Form(""),
    From: str = Form(""),
    To: str = Form(""),
    x_twilio_signature: str = Header(default=""),
):
    if TWILIO_WEBHOOK_URL and TWILIO_AUTH_TOKEN:
        form = dict(await request.form())
        if not RequestValidator(TWILIO_AUTH_TOKEN).validate(TWILIO_WEBHOOK_URL, form, x_twilio_signature):
            logger.warning("Rejected /sms call with an invalid Twilio signature")
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    return await process_incoming_message(From, Body)


@router.post("/send")
async def send_message(
    to: str = Body(..., embed=True),
    body: str = Body(..., embed=True),
    x_bot_key: str = Header(default=""),
):
    """Internal endpoint used by the backend to send WhatsApp messages."""
    if BOT_API_KEY and not secrets.compare_digest(x_bot_key, BOT_API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing bot key")
    ok = send_whatsapp_message(to, body)
    return {"ok": ok}
