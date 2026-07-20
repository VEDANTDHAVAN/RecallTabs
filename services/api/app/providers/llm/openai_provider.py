from __future__ import annotations

import json
from typing import Any, AsyncGenerator

from openai import AsyncOpenAI

from app.providers.llm.base import BaseLLMProvider
from app.providers.llm.config import ProviderConfig

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, config: ProviderConfig):
        self.config = config

        self.client = AsyncOpenAI(
            api_key=config.api_key, timeout=config.timeout,
            base_url=config.base_url,
        )

    def _messages(self, system: str | None, user: str):
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": user})

        return messages
    
    async def chat(self, *, system: str | None = None,
        user: str, **kwargs: Any,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.config.model, messages=self._messages(system, user),
            **self.config.generate_kwargs(), **kwargs,
        )

        return response.choices[0].message.content or ""
    
    async def stream_chat(self, *, system: str | None, user: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.config.model, messages=self._messages(system, user),
            stream=True, **self.config.generate_kwargs(), **kwargs,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta.content

            if delta:
                yield delta

    async def json_chat(self, *, system: str | None = None, user: str, **kwargs: Any) -> dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=self.config.model, messages=self._messages(system, user), **kwargs,
            response_format={"type": "json_object"}, **self.config.generate_kwargs(),
        )

        return json.loads(
            response.choices[0].message.content or "{}"
        )
    
    async def health(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False
        
    async def list_models(self) -> list[str]:
        models = await self.client.models.list()
        return sorted(m.id for m in models.data)