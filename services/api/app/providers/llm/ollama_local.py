from __future__ import annotations

import json
from typing import Any, AsyncGenerator

from openai import AsyncOpenAI

from app.providers.llm.base import BaseLLMProvider
from app.providers.llm.config import ProviderConfig

class OllamaProvider(BaseLLMProvider):
    def __init__(self, config: ProviderConfig):
        super().__init__(config)

        self.client = AsyncOpenAI(
            api_key="ollama", base_url=config.base_url.rstrip("/")
            if config.base_url else "http://localhost:11434/v1",
        )

    async def chat(
        self, *, system: str | None = None, user: str, **kwargs: Any
    ) -> str:
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        response = await self.client.chat.completions.create(
            model=self.config.model, messages=messages,
            stream=False, **kwargs,
        )

        return response.choices[0].message.content or ""
    
    async def stream_chat(self, *, system: str | None, user: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        stream = await self.client.chat.completions.create(
            model=self.config.model, messages=messages,
            stream=True, **kwargs,
        )

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                yield delta

    async def completion(self, prompt: str, **kwargs: Any) -> str:
        return await self.chat(system=None, user=prompt, **kwargs)
    
    async def json_chat(self, *, system: str | None = None, user: str, **kwargs: Any) -> dict[str, Any]:
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        response = await self.client.chat.completions.create(
            model=self.config.model, messages=messages,
            response_format={"type": "json_object"},
            stream=False, **kwargs,
        )

        return json.loads(response.choices[0].message.content or "{}")
    
    async def list_models(self) -> list[str]:
        models = await self.client.models.list()
        return sorted(model.id for model in models.data)
    
    async def health(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False