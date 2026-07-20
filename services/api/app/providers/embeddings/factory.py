from app.providers.embeddings.base import BaseEmbeddingProvider
from app.providers.embeddings.config import EmbeddingProviderConfig

from app.providers.embeddings.openai_provider import OpenAIEmbeddingProvider
from app.providers.embeddings.ollama_provider import OllamaEmbeddingProvider
from app.providers.embeddings.cohere_provider import CohereEmbeddingProvider
from app.providers.embeddings.sentence_transformers_provider import SentenceTransformerProvider

class EmbeddingProviderFactory:
    _providers = {
        "openai": OpenAIEmbeddingProvider,
        "ollama": OllamaEmbeddingProvider,
        "cohere": CohereEmbeddingProvider,
        "sentence-transformers": SentenceTransformerProvider,
    }

    @classmethod
    def create(cls, config: EmbeddingProviderConfig) -> BaseEmbeddingProvider:
        provider = cls._providers.get(config.provider.lower())

        if provider is None:
            raise ValueError(
                f"Unsupported embedding provider: {config.provider}"
            )
        
        return provider(config)