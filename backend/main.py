from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# List of allowed origins
origins = [
    "http://localhost",
    "http://localhost:3000",  # Example: if your frontend is running on this port
    "http://127.0.0.1:8000",
    # Add any other origins that need access
]

# Adding CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins that are allowed to make requests
    allow_credentials=True,  # Allow cookies to be sent in cross-origin requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers to be sent in requests
)

from fastapi import APIRouter
from routers import upload, chat

app.include_router(upload.router)
app.include_router(chat.router)

