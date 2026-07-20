from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

from app.providers.llm.config import ProviderConfig

class BaseLLMProvider(ABC):
    def __init__(self, config: ProviderConfig):
        self.config = config

    @abstractmethod
    async def chat(self, *, system: str | None, user: str, **kwargs: Any) -> str:
        pass

    @abstractmethod
    async def stream_chat(self, *, system: str | None, user: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    async def completion(self, prompt: str, **kwargs: Any) -> str:
        pass

    @abstractmethod
    async def json_chat(self, *, system: str | None = None, user: str, **kwargs: Any) -> dict[str, Any]:
        pass

    @abstractmethod
    async def health(self) -> bool:
        pass

    @abstractmethod
    async def list_models(self) -> list[str]:
        pass