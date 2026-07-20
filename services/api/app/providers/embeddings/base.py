from __future__ import annotations

from abc import ABC, abstractmethod

class BaseEmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        pass

    @abstractmethod
    async def health(self) -> bool:
        pass

    @abstractmethod
    async def list_models(self) -> list[str]:
        pass