import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Optional

import requests

from app.core.config import settings

logger = logging.getLogger("tisdan.bot_notify")

# WhatsApp sends go through a small pool so broadcasts to many recipients
# don't block the HTTP request that triggered them.
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="whatsapp")


def _bot_url() -> Optional[str]:
    if settings.TISDAN_BOT_URL:
        return str(settings.TISDAN_BOT_URL).rstrip("/")
    if settings.ENVIRONMENT == "local":
        return "http://127.0.0.1:8001"
    return None


def send_whatsapp_via_bot(to: str, body: str) -> bool:
    """Send a WhatsApp message via the bot service's /send endpoint.

    Always logs the outcome so failures are visible instead of silent.
    """
    bot_url = _bot_url()
    if not bot_url:
        logger.warning("WhatsApp send skipped: TISDAN_BOT_URL is not set.")
        return False

    url = bot_url + "/send"
    headers = {"X-Bot-Key": settings.BOT_API_KEY} if settings.BOT_API_KEY else {}
    try:
        resp = requests.post(url, json={"to": to, "body": body}, headers=headers, timeout=10)
        if resp.status_code != 200:
            logger.warning("WhatsApp send failed: bot returned HTTP %s - %s", resp.status_code, resp.text)
            return False
        ok = resp.json().get("ok", False)
        if not ok:
            logger.warning(
                "WhatsApp send failed: bot reported ok=False for %s "
                "(check TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN on the bot service)",
                to,
            )
        return ok
    except requests.exceptions.ConnectionError as exc:
        logger.warning("WhatsApp send failed: could not reach bot at %s. Is tisdan-bot running? (%s)", url, exc)
        return False
    except Exception as exc:
        logger.warning("WhatsApp send failed: %s", exc)
        return False


def queue_whatsapp(phones: Iterable[Optional[str]], body: str) -> int:
    """Send `body` to every distinct, valid phone number in the background.
    Returns how many sends were queued."""
    targets = {format_phone(p) for p in phones}
    targets.discard(None)
    for to in targets:
        _executor.submit(send_whatsapp_via_bot, to, body)
    return len(targets)


def format_phone(number: Optional[str]) -> Optional[str]:
    if not number:
        return None
    s = number.strip()
    if not s:
        return None

    # Allow full WhatsApp URIs or normalized phone numbers
    if s.startswith("whatsapp:"):
        return s

    # Remove spaces, dashes, and parentheses
    s = s.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    if s.startswith("0") and len(s) >= 10:
        # Assume Nigerian local number and normalize to +234
        s = "+234" + s[1:]
    elif s.startswith("234") and not s.startswith("+234"):
        s = "+" + s
    elif not s.startswith("+"):
        s = "+" + s

    return s
