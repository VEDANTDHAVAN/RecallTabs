from app.infrastructure.database.models.message import Message

from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.context_selection_service import ContextSelectionService

from app.repositories.message_repository import MessageRepository
from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.memory_cluster_repository import MemoryClusterRepository

class ConversationService:
    def __init__(self, chunk_repository: TabChunkRepository,
        message_repository: MessageRepository, session_repository: SessionRepository,
        cluster_repository: MemoryClusterRepository,
    ):
        self.chunk_repository = chunk_repository
        self.message_repository = message_repository
        self.embedder = EmbeddingService()
        self.llm = LLMService()
        self.context_selector = ContextSelectionService(
            chunk_repository, session_repository, cluster_repository,
        )

    def chat(self, conversation_id: str, question: str):
        self.message_repository.create(
            Message(
                conversation_id=conversation_id, 
                role="user", content=question,
            )
        )

        seen = set()
        sources = []

        context = self.context_selector.build_context(question)

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
    
    def stream_chat(
        self, question: str,
        conversation_id: str,
    ):
        embedding = self.embedder.embed(question)

        chunks = self.chunk_repository.search_chunks(embedding)

        context = "\n\n".join(
            chunk["chunk_text"][:1000]
            for chunk in chunks
            if chunk["chunk_text"]
        )

        messages = self.message_repository.get_messages(conversation_id)

        history = [
            {
                "role": message.role,
                "content": message.content,
            } for message in messages
        ]

        # save user message immediately
        self.message_repository.create(
            Message(
                conversation_id=conversation_id,
                role="user", content=question,
            )
        )

        answer = ""

        for token in self.llm.stream_chat(
            question=question, context=context,
            history=history,
        ):
            answer += token
            yield token

        # save assistant response after streaming completes
        self.message_repository.create(
            Message(
                conversation_id=conversation_id,
                role="assistant", content=answer,
            )
        )