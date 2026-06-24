# FastAPI + Twilio SMS Reply

A minimal FastAPI application that replies to incoming Twilio SMS messages.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app:app --reload
```

## Configure Twilio

1. Expose your app with a public URL (for example using ngrok).
2. In Twilio Console, set the SMS webhook for your phone number to `POST https://<your-host>/sms`.
3. When a message arrives, the app replies with a simple acknowledgement.
