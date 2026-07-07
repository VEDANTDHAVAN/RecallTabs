import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path = [p for p in sys.path if p != str(Path(__file__).resolve().parent)]

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
