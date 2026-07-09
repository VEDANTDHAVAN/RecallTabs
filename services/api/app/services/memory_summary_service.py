from app.services.llm_service import LLMService

class MemorySummaryService:
    def __init__(self):
        self.llm = LLMService()

    def summarize(
        self, texts: list[str],
    ) -> str:
        prompt = """Summarize these browsing memories.

Focus on:

Main topic

Important concepts

Overall learning

Maximum 200 words."""

        joined = "\n\n".join(texts)

        return self.llm.chat(
            question="Summarize these browsing memories.",
            context=joined, history=[],
        ) 