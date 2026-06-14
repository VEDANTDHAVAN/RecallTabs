from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logger import configure_logging

configure_logging()

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }