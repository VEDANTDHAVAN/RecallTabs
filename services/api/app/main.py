from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logger import configure_logging
from app.api.v1.tabs import router as tabs_router

configure_logging()

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(tabs_router)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }