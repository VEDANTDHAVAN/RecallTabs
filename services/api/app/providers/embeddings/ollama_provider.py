from __future__ import annotations

from openai import AsyncOpenAI

from app.providers.embeddings.base import BaseEmbeddingProvider
from app.providers.embeddings.config import EmbeddingProviderConfig


class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, config: EmbeddingProviderConfig):
        self.config = config

        self.client = AsyncOpenAI(
            api_key=config.api_key or "ollama",
            base_url=config.base_url,
            timeout=config.timeout,
        )

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        response = await self.client.embeddings.create(
            model=self.config.model,
            input=text,
        )

        return response.data[0].embedding

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        response = await self.client.embeddings.create(
            model=self.config.model,
            input=texts,
        )

        return [item.embedding for item in response.data]

    async def health(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        models = await self.client.models.list()
        return [m.id for m in models.data]