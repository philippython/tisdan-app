# Tisdan WhatsApp Bot

FastAPI service that answers patients and coordinators on WhatsApp (via Twilio) and delivers messages on behalf of the backend. See [../DEPLOYMENT.md](../DEPLOYMENT.md) for the full setup.

## Run locally

```bash
cp .env.example .env        # set API_BASE, BOT_API_KEY and Twilio credentials
pip install -r requirements.txt
uvicorn main:app --port 8001 --reload
```

## Endpoints

- `POST /sms`: Twilio webhook for incoming WhatsApp messages. Set it in the Twilio Console as `https://<bot-host>/sms` (POST).
- `POST /send`: internal endpoint the backend calls to push a message. Requires the `X-Bot-Key` header.
- `GET /health`: liveness check.

## Tests

```bash
python -m unittest discover -s tests -v
```

This starts the real backend (from `../tisdan-backend`) on a temporary database and runs complete WhatsApp conversations against it.
