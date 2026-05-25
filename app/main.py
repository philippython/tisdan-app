from fastapi import FastAPI
from app.routes.main import router as api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
