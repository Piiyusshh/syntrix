from fastapi import FastAPI

app = FastAPI(
    title="Syntrix API",
    version="0.1.0"
)


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