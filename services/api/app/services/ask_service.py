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

        for chunk in chunks:
            print("\nTITLE:", chunk["title"])
            print("\nCONTENT:")
            print(chunk["chunk_text"][:500])
            print("\n---------") 

        context = "\n\n".join(
            chunk["chunk_text"][:1000] for chunk in chunks
            if chunk["chunk_text"]
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

        print("=" * 20)
        print("\nCONTEXT\n")
        print(context[:3000])
        print("=" * 20)

        return {
            "answer": answer, "sources": sources
        }