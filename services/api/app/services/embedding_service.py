import os
from openai import OpenAI
from ollama import Client

from app.core.config import get_settings

from app.providers.embeddings.config import EmbeddingProviderConfig
from app.providers.embeddings.factory import EmbeddingProviderFactory

class EmbeddingLLMService:
    def __init__(self):
        settings = get_settings()
        # self.client = OpenAI(api_key=settings.OPENAI_API_KEY,)
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )
        self.model = "text-embedding-3-small"

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=384,
        )

        return response.data[0].embedding

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=384,
        )

        return [
            item.embedding
            for item in response.data
        ]
    
class EmbeddingService:
    def __init__(self, config: EmbeddingProviderConfig):
        self.provider = EmbeddingProviderFactory.create(config)

    async def embed(self, text: str):
        return await self.provider.embed(text)
    
    async def embed_batch(self, texts: list[str]):
        return await self.provider.embed_batch(texts)
    
    async def health(self):
        return await self.provider.health()
    
    async def list_models(self):
        return await self.provider.list_models()