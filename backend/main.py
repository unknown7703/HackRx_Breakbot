from fastapi import FastAPI

app = FastAPI()

# TODO: Need to add the routers here

from fastapi import APIRouter
from routers import upload, ask

app.include_router(upload.router, tags=["upload"])
app.include_router(ask.router, tags=["ask"])
