import os
from typing import Optional

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

client: Optional[Client] = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_whatsapp_message(to: str, body: str) -> bool:
    if client is None:
        return False

    normalized_to = to.strip()
    if normalized_to.startswith("whatsapp:"):
        whatsapp_to = normalized_to
    else:
        if not normalized_to.startswith("+"):
            normalized_to = "+" + normalized_to
        whatsapp_to = f"whatsapp:{normalized_to}"

    try:
        client.messages.create(body=body, from_=TWILIO_WHATSAPP_FROM, to=whatsapp_to)
        return True
    except TwilioRestException:
        return False
