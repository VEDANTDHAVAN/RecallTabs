from app.infrastructure.database.models.message import Message

from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService

from app.repositories.message_repository import MessageRepository
from app.repositories.tab_chunk_repository import TabChunkRepository

class ConversationService:
    def __init__(self, chunk_repository: TabChunkRepository,
        message_repository: MessageRepository,
    ):
        self.chunk_repository = chunk_repository
        self.message_repository = message_repository
        self.embedder = EmbeddingService()
        self.llm = LLMService()

    def chat(self, conversation_id: str, question: str):
        self.message_repository.create(
            Message(
                conversation_id=conversation_id, 
                role="user", content=question,
            )
        )

        seen = set()
        sources = []

        embedding = self.embedder.embed(question)

        chunks = self.chunk_repository.search_chunks(embedding)

        for chunk in chunks:
            if chunk["url"] in seen:
                continue

            seen.add(chunk["url"])

            sources.append({
                "title": chunk["title"],
                "url": chunk["url"],
            })

        context = "\n\n".join(
            chunk["chunk_text"][:1000]
            for chunk in chunks
            if chunk["chunk_text"]
        )

        messages = self.message_repository.get_messages(conversation_id)

        history = [{
            "role": m.role, "content": m.content,
        } for m in messages]

        answer = self.llm.chat(
            question=question, context=context,
            history=history,
        )

        self.message_repository.create(
            Message(
                conversation_id=conversation_id,
                role="assistant", content=answer, sources=sources
            )
        )

        return {
            "answer": answer,
            "sources": sources,
        }