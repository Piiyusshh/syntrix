from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.documents import router as document_router
from app.api.users import router as user_router

app = FastAPI(
    title="Syntrix API",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Syntrix API"
    }