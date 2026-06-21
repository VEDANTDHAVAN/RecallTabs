from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logger import configure_logging
from app.api.v1.tabs import router as tabs_router
from app.api.v1.search import router as search_router
from app.api.v1.ask import router as ask_router
from app.api.v1.related import router as related_router

configure_logging()

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(tabs_router, prefix="/api/v1",)
app.include_router(search_router, prefix="/api/v1",)
app.include_router(ask_router, prefix="/api/v1",)
app.include_router(related_router, prefix="/api/v1", tags=["Related Tabs"])

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "chrome-extension://*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }