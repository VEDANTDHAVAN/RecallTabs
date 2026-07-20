from __future__ import annotations

from sentence_transformers import SentenceTransformer

from app.providers.embeddings.base import BaseEmbeddingProvider
from app.providers.embeddings.config import EmbeddingProviderConfig


class SentenceTransformerProvider(BaseEmbeddingProvider):
    def __init__(self, config: EmbeddingProviderConfig):
        self.model = SentenceTransformer(config.model)

    async def embed(self, text: str) -> list[float]:
        return self.model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self.model.encode(
            texts,
            normalize_embeddings=True,
        ).tolist()

    async def health(self) -> bool:
        return True

    async def list_models(self) -> list[str]:
        return [self.model.model_card_data.base_model or self.model.__class__.__name__]