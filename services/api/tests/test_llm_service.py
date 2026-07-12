import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path = [p for p in sys.path if p != str(Path(__file__).resolve().parent)]

from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService


class DummyMessage:
    def __init__(self, content):
        self.content = content


class DummyChoice:
    def __init__(self, content):
        self.message = DummyMessage(content)


class DummyResponse:
    def __init__(self, content):
        self.choices = [DummyChoice(content)]


def test_chat_returns_empty_string_when_completion_content_is_none(monkeypatch):
    def fake_create(**kwargs):
        return DummyResponse(None)

    monkeypatch.setattr(
        "app.services.llm_service.client.chat.completions.create",
        fake_create,
    )

    service = LLMService()

    assert service.chat("question", "context", []) == ""


def test_embedding_service_uses_settings_api_key(monkeypatch):
    class DummyClient:
        def __init__(self, **kwargs):
            self.api_key = kwargs.get("api_key")

    monkeypatch.setattr("app.services.embedding_service.OpenAI", DummyClient)
    monkeypatch.setattr(
        "app.services.embedding_service.get_settings",
        lambda: type("Settings", (), {"OPENAI_API_KEY": "test-key"})(),
    )

    service = EmbeddingService()

    assert service.client.api_key == "test-key"


def test_embed_requests_384_dimensions(monkeypatch):
    captured_kwargs = {}

    class DummyEmbeddings:
        def create(self, **kwargs):
            captured_kwargs.update(kwargs)
            return type(
                "Response",
                (),
                {"data": [type("Item", (), {"embedding": [0.1, 0.2]})()]},
            )()

    class DummyClient:
        def __init__(self, **kwargs):
            self.api_key = kwargs.get("api_key")
            self.embeddings = DummyEmbeddings()

    monkeypatch.setattr("app.services.embedding_service.OpenAI", DummyClient)
    monkeypatch.setattr(
        "app.services.embedding_service.get_settings",
        lambda: type("Settings", (), {"OPENAI_API_KEY": "test-key"})(),
    )

    service = EmbeddingService()
    service.embed("hello")

    assert captured_kwargs["dimensions"] == 384
