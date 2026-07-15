from ollama import Client
from app.core.config import settings
from app.providers.base import BaseLLMProvider

class OllamaLocalProvider(BaseLLMProvider):
    def __init__(self):
        self.client = Client(
            host=settings.OLLAMA_HOST,
        )

        self.model = settings.OLLAMA_MODEL

    def chat(self, *, system: str, user: str) -> str:
        response = self.client.chat(
            model=self.model, messages=[
                {
                    "role": "system", "content": system,
                },
                {
                    "role": "user", "content": user,
                },
            ], format="json",
        )

        return response["message"]["content"]
    
    def stream_chat(self, *, system: str, user: str):
        stream = self.client.chat(
            model=self.model, stream=True,
            messages=[
                {
                    "role": "system", "content": system,
                },
                {
                    "role": "user", "content": user,
                },
            ],
        )

        for chunk in stream:
            yield chunk["message"]["content"]

    def completion(self, prompt: str) -> str:
        return self.chat(
            system="", user=prompt,
        )