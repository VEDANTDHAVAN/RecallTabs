from typing import Generator

from app.providers.ollama_local import OllamaLocalProvider

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
    def __init__(self):
        self.provider = OllamaLocalProvider()

    def answer(self, question: str, context: str) -> str:
        prompt = f"""
Context: {context}
Question: {question}

Answer ONLY using the context above.
"""
        return self.provider.chat(
            system=SYSTEM_PROMPT, user=prompt,
        )
    
    def complete(self, prompt: str) -> str:
        return self.provider.chat(
            system="Return valid JSON only.", user=prompt,
        )
    
    def chat(
        self, question: str, context: str,
        history: list[dict],
    ) -> str:
        history_text = ""

        for message in history:
            history_text += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        prompt = f"""
Conversation History: {history_text}

Retrieved Context: {context}

Current Question: {question}
"""
        return self.provider.chat(
            system=SYSTEM_PROMPT, user=prompt,
        )
    
    def stream_chat(
        self, question: str, context: str,
        history: list[dict],
    ) -> Generator[str, None, None]:
        history_text = ""

        for message in history:
            history_text += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        prompt = f"""
Conversation History: {history_text}

Retrieved Context: {context}

Current Question: {question}
"""
        yield from self.provider.stream_chat(
            system=SYSTEM_PROMPT, user=prompt,
        )

    def json_chat(self, prompt: str) -> str:
        return self.provider.chat(
            system="Return valid JSON only.", user=prompt,
        )