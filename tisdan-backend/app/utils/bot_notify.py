import os
import requests
from typing import Optional

TISDAN_BOT_URL = os.getenv("TISDAN_BOT_URL")


def send_whatsapp_via_bot(to: str, body: str) -> bool:
    """Send a WhatsApp message via the external bot service.

    Expects `TISDAN_BOT_URL` environment variable to be set to the bot base URL
    (e.g. https://bot.example.com). Posts JSON {to, body} to /send.
    """
    if not TISDAN_BOT_URL:
        return False

    url = TISDAN_BOT_URL.rstrip("/") + "/send"
    try:
        resp = requests.post(url, json={"to": to, "body": body}, timeout=10)
        return resp.status_code == 200 and resp.json().get("ok", False)
    except Exception:
        return False


def format_phone(number: Optional[str]) -> Optional[str]:
    if not number:
        return None
    s = number.strip()
    if s.startswith("whatsapp:"):
        return s
    if not s.startswith("+"):
        s = "+" + s
    return s
