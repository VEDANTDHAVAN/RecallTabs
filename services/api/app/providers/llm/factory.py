from __future__ import annotations

from app.providers.llm.base import BaseLLMProvider
from app.providers.llm.config import ProviderConfig
from app.providers.llm.ollama_local import OllamaProvider
from app.providers.llm.openai_provider import OpenAIProvider
from app.providers.llm.gemini_provider import GeminiProvider

class ProviderFactory:
    _providers: dict[str, type[BaseLLMProvider]] = {
        "ollama": OllamaProvider, 
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
    }

    @classmethod
    def create(cls, config: ProviderConfig) -> BaseLLMProvider:
        provider_cls = cls._providers.get(config.provider.lower())

        if provider_cls is None:
            supported = ", ".join(sorted(cls._providers))
            raise ValueError(
                f"Unsupported provider '{config.provider}'. "
                f"Supported providers: {supported}"
            )
        
        return provider_cls(config)
    
    @classmethod
    def register(cls, name: str, provider: type[BaseLLMProvider]) -> None:
        cls._providers[name.lower()] = provider

    @classmethod
    def unregister(cls, name: str) -> None:
        cls._providers.pop(name.lower(), None)

    @classmethod
    def supported_providers(cls) -> list[str]:
        return sorted(cls._providers.keys())
