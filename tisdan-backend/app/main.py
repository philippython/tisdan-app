import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.config import settings
from app.database.db import engine, init_db
from app.routes.main import router as api_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    # e.g. a duplicate email/branch code, or deleting a record that other
    # records still point to
    return JSONResponse(
        status_code=409,
        content={
            "detail": "This change conflicts with existing data (duplicate value, "
            "or the record is still linked to other records)."
        },
    )


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        init_db(session)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}
