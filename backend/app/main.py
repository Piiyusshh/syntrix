from fastapi import FastAPI

from app.api.users import router as user_router

app = FastAPI(
    title="Syntrix API",
    version="0.1.0"
)

app.include_router(user_router)


@app.get("/")
def root():
    return {
        "application": "Syntrix",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }