from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService

class AskService:
    def __init__(self, repository):
        self.repository = repository
        self.embedder = EmbeddingService()
        self.llm = LLMService()

    def ask(self, question: str):
        embedding = self.embedder.embed(question)

        chunks = self.repository.search_chunks(embedding)

        context = "\n\n".join(
            chunk["content"][:1000] for chunk in chunks
            if chunk["content"]
        )

        answer = self.llm.answer(
            question, context
        )

        seen = set()
        sources = []

        for chunk in chunks:
            if chunk["url"] in seen:
                continue

            seen.add(chunk["url"])

            sources.append({
                "title": chunk["title"],
                "url": chunk["url"]
            })

        return {
            "answer": answer, "sources": sources
        }