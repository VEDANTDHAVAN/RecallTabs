from typing import Any, cast

from cohere import AsyncClient

from app.providers.embeddings.base import BaseEmbeddingProvider
from app.providers.embeddings.config import EmbeddingProviderConfig


class CohereEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, config: EmbeddingProviderConfig):
        self.config = config
        self.client = AsyncClient(api_key=config.api_key)

    async def embed(self, text: str) -> list[float]:
        response = await self.client.embed(
            texts=[text],
            model=self.config.model,
            input_type="search_document",
            embedding_types=["float"],
        )

        embeddings = cast(Any, response.embeddings)

        if isinstance(embeddings, list):
            return embeddings[0]

        return embeddings.float[0]

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        response = await self.client.embed(
            texts=texts,
            model=self.config.model,
            input_type="search_document",
            embedding_types=["float"],
        )

        embeddings = cast(Any, response.embeddings)

        if isinstance(embeddings, list):
            return embeddings

        return embeddings.float

    async def health(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        models = await self.client.models.list()
        return [m.name for m in models.models if m.name]