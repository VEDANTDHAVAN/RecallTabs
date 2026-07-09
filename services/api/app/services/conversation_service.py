from datetime import datetime

from app.infrastructure.database.models.message import Message

from app.services.llm_service import LLMService
from app.services.context_selection_service import ContextSelectionService, ContextChunk
from app.services.memory_importance_service import MemoryImportanceService
from app.services.graph_context_service import GraphContextService

from app.repositories.message_repository import MessageRepository
from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.memory_cluster_repository import MemoryClusterRepository
from app.repositories.tab_repository import TabRepository
from app.repositories.topic_repository import TopicRepository

class ConversationService:
    def __init__(
        self,
        chunk_repository: TabChunkRepository,
        message_repository: MessageRepository,
        session_repository: SessionRepository,
        cluster_repository: MemoryClusterRepository,
        tab_repository: TabRepository,
        topic_repository: TopicRepository,
        graph_context_service: GraphContextService,
    ):
        self.chunk_repository = chunk_repository
        self.message_repository = message_repository
        self.tab_repository = tab_repository
        self.topic_repository = topic_repository

        self.llm = LLMService()
        self.memory_service = MemoryImportanceService()

        self.context_selector = ContextSelectionService(
            chunk_repository=chunk_repository, session_repository=session_repository,
            cluster_repository=cluster_repository, topic_repository=topic_repository,
            graph_context_service=graph_context_service,
        )

    def _update_memory_scores(self, chunks: list[ContextChunk]):
        """
        Increase importance score for tabs that were actually
        used while answering the question.
        """

        used_tabs = set()

        for chunk in chunks:

            tab_id = chunk["tab_id"]

            if tab_id in used_tabs:
                continue

            used_tabs.add(tab_id)

            tab = self.tab_repository.get_by_id(tab_id)

            if not tab:
                continue

            tab.chat_reference_count += 1
            tab.last_chat_at = datetime.utcnow()

            self.memory_service.calculate(tab)

            self.tab_repository.update(tab)

            if tab.topic_id:
                self.topic_repository.increment_importance(tab.topic_id)

    def chat(
        self,
        conversation_id: str,
        question: str,
    ):
        # Save user message
        self.message_repository.create(
            Message(
                conversation_id=conversation_id,
                role="user",
                content=question,
            )
        )

        # Retrieve context
        context_data = self.context_selector.build_context(question)

        context = context_data["context"]
        chunks = context_data["chunks"]

        # Conversation history
        messages = self.message_repository.get_messages(
            conversation_id
        )

        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

        # Ask LLM
        answer = self.llm.chat(
            question=question,
            context=context,
            history=history,
        )

        # Sources
        seen = set()
        sources = []

        for chunk in chunks:
            url = chunk["url"]

            if url in seen:
                continue

            seen.add(url)

            sources.append(
                {
                    "title": chunk["title"],
                    "url": url,
                }
            )

        self._update_memory_scores(chunks)

        # Save assistant response
        self.message_repository.create(
            Message(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
                sources=sources,
                importance=self.memory_service.calculate(
                    question, answer, sources,
                ),
            )
        )

        return {
            "answer": answer,
            "sources": sources,
        }

    def stream_chat(
        self,
        question: str,
        conversation_id: str,
    ):
        context_data = self.context_selector.build_context(
            question
        )

        context = context_data["context"]
        chunks = context_data["chunks"]

        messages = self.message_repository.get_messages(
            conversation_id
        )

        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

        # Save user message
        self.message_repository.create(
            Message(
                conversation_id=conversation_id,
                role="user",
                content=question,
            )
        )

        answer = ""

        for token in self.llm.stream_chat(
            question=question,
            context=context,
            history=history,
        ):
            answer += token
            yield token

        seen = set()
        sources = []

        for chunk in chunks:
            url = chunk["url"]

            if url in seen:
                continue

            seen.add(url)

            sources.append(
                {
                    "title": chunk["title"],
                    "url": url,
                }
            )

        self._update_memory_scores(chunks)

        # Save assistant message
        self.message_repository.create(
            Message(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
                sources=sources,
                importance=self.memory_service.calculate(
                    question, answer, sources,
                ),
            )
        )
