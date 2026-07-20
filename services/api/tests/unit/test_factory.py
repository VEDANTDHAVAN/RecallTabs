from app.providers.llm.config import ProviderConfig
from app.providers.llm.factory import ProviderFactory
from app.providers.llm.ollama_local import OllamaProvider

def test_create_ollama():
    config = ProviderConfig(
        provider="ollama", model="phi3:mini",
        base_url="http://localhost:11434/v1",
    )

    provider = ProviderFactory.create(config)

    assert isinstance(provider, OllamaProvider)