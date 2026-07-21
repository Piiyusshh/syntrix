from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversation_router
from app.api.documents import router as document_router
from app.api.users import router as user_router

app = FastAPI(
    title="Syntrix API",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(document_router)
app.include_router(conversation_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Syntrix API"
    }