from fastapi import FastAPI

from service.routes import router

app = FastAPI()
app.include_router(router)
