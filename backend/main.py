from fastapi import FastAPI
from phi.assistant import Assistant

app = FastAPI()

from fastapi import APIRouter
from routers import upload, ask

app.include_router(upload.router)
app.include_router(ask.router)



