from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RecallTabs API"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = ""
    LLM_PROVIDER: str = "ollama"
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "phi3:mini"
    OPENAI_API_KEY: str = ""
    OLLAMA_API_KEY: str | None = None

    CLERK_JWKS_URL: str = ""
    CLERK_ISSUER: str = ""
    CLERK_AUDIENCE: str = ""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()