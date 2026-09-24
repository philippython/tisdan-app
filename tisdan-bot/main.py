import logging

from dotenv import load_dotenv

# Load .env before the service modules read their configuration
load_dotenv()

from fastapi import FastAPI  # noqa: E402

from service.routes import router  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI(title="tisdan-bot")
app.include_router(router)
