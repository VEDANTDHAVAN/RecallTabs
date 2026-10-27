from app.providers.embeddings.config import EmbeddingProviderConfig
from app.core.config import settings
from app.services.embedding_service import EmbeddingService

def get_embedding_service() -> EmbeddingService:
    config = EmbeddingProviderConfig(
        provider="openai", model="text-embedding-3-small",
        api_key=settings.OPENAI_API_KEY, dimensions=1536,
    )

    return EmbeddingService(config)