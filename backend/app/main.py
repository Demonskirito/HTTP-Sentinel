from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.history import router as history_router


app = FastAPI(
    title="AI-WebSec-Assistant",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(history_router)


@app.get("/")
def root():
    return {
        "name": "AI-WebSec-Assistant",
        "version": "0.1.0",
        "status": "running"
    }