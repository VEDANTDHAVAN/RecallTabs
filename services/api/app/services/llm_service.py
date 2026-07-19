from collections.abc import AsyncGenerator

from app.providers.config import ProviderConfig
from app.providers.factory import ProviderFactory

SYSTEM_PROMPT = """
You are RecallTabs.

You answer questions using the user's saved browser memory.

Always prioritize:
1. Retrieved browsing context
2. Previous conversation

If the answer cannot be found in the provided context, reply exactly:
I couldn't find that information in your saved tabs.

Be concise and factual.
"""

class LLMService:
    def __init__(self, config: ProviderConfig | None = None):
        if config is None:
            config = ProviderConfig(
                provider="ollama", model="phi3:mini",
                base_url="http://localhost:11434/v1",
            )

        self.provider = ProviderFactory.create(config)

    async def answer(self, question: str, context: str,) -> str:
        prompt = f"""
Context: {context}

Question: {question}

Answer ONLY using the context above.
"""
        return await self.provider.chat(
            system=SYSTEM_PROMPT, user=prompt,
        )
    
    async def complete(self, prompt: str) -> str:
        return await self.provider.completion(prompt)
    
    async def chat(
        self, question: str, context: str, history: list[dict],
    ) -> str:
        history_text = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in history
        )

        prompt = f"""
Conversation History: {history_text}

Retrieved Context: {context}

Current Question: {question}
"""
        return await self.provider.chat(
            system=SYSTEM_PROMPT, user=prompt
        )
    
    async def stream_chat(
        self, question: str, context: str, history: list[dict],
    ) -> AsyncGenerator[str, None]:
        history_text = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in history
        )

        prompt = f"""
Conversation History: {history_text}

Retrieved Context: {context}

Current Question: {question}
"""
        stream = await self.provider.stream_chat(
            system=SYSTEM_PROMPT, user=prompt,
        )

        async for chunk in stream:
            yield chunk

    async def json_chat(self, prompt: str) -> dict:
        return await self.provider.json_chat(
            system="Return valid JSON only.", user=prompt,
        )
    
    async def health(self) -> bool:
        return await self.provider.health()
    
    async def list_models(self) -> list[str]:
        return await self.provider.list_models()