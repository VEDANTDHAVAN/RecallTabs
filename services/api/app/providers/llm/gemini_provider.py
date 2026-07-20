from __future__ import annotations

import json 
from typing import Any, AsyncGenerator

from google import genai

from app.providers.llm.base import BaseLLMProvider
from app.providers.llm.config import ProviderConfig

class GeminiProvider(BaseLLMProvider):
    def __init__(self, config: ProviderConfig):
        self.config = config

        self.client = genai.Client(
            api_key=config.api_key,
        )

    def _prompt(self, system: str | None, user: str) -> str:
        if system:
            return f"{system}\n\n{user}"
        
        return user
    
    async def chat(
        self, *, system: str | None = None,
        user: str, **kwargs: Any,
    ) -> str:
        response = await self.client.aio.models.generate_content(
            model=self.config.model, contents=self._prompt(system, user),
        )

        return response.text or ""
    
    async def stream_chat(self, *, system: str | None, user: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        stream = await self.client.aio.models.generate_content_stream(
            model=self.config.model, contents=self._prompt(system, user),
        )
        
        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    async def completion(self, prompt: str, **kwargs: Any) -> str:
        response = await self.client.aio.models.generate_content(
            model=self.config.model, contents=prompt,
        )

        return response.text or ""
    
    async def json_chat(self, *, system: str | None = None, user: str, **kwargs: Any) -> dict[str, Any]:
        text = await self.chat(
            system=system, user=user, **kwargs
        )

        return json.loads(text)
    
    async def health(self) -> bool:
        try:
            await self.client.aio.models.list()
            return True
        except Exception:
            return False
        
    async def list_models(self) -> list[str]:
        models = []
        pager = await self.client.aio.models.list()

        async for model in pager:
            models.append(model.name)

        return sorted(models)