from typing import TypedDict

from app.services.embedding_service import EmbeddingService
from app.services.graph_context_service import GraphContextService
from app.services.retrieval_intent_service import RetrievalIntent, RetrievalIntentService

class ContextChunk(TypedDict):
    tab_id: str
    title: str
    url: str
    chunk_text: str
    score: float

class ContextResult(TypedDict):
    context: str
    chunks: list[ContextChunk]

class ContextSelectionService:
    def __init__(
        self, chunk_repository, topic_repository,
        session_repository, cluster_repository, 
        graph_context_service: GraphContextService,
    ):
        self.chunk_repository = chunk_repository
        self.session_repository = session_repository
        self.cluster_repository = cluster_repository
        self.topic_repository = topic_repository
        
        self.graph_context = graph_context_service

        self.embedder = EmbeddingService()
        self.intent_service = RetrievalIntentService()

    def build_context(self, question: str) -> ContextResult:
        embedding = self.embedder.embed(question)

        intent = self.intent_service.classify(question)

        related_entities = self.graph_context.expand(question)

        clusters = []
        sessions = []
        topics = []

        # Adaptive Retrieval
        if intent == RetrievalIntent.RESEARCH:
            topics = self.topic_repository.search_by_embedding(
                embedding, limit=5,
            )

            chunks = self.chunk_repository.search_chunks(
                embedding, limit=15,
            )

        elif intent == RetrievalIntent.HISTORY:
            sessions = self.session_repository.search_by_embedding(
                embedding, limit=5,
            )

            clusters = self.cluster_repository.search_by_embedding(
                embedding, limit=5,
            )

            chunks = self.chunk_repository.search_chunks(
                embedding, limit=10,
            )
        
        elif intent == RetrievalIntent.BROWSING:
            sessions = self.session_repository.search_by_embedding(
                embedding, limit=6,
            )

            chunks = self.chunk_repository.search_chunks(
                embedding, limit=8,
            )

        else:
            clusters = self.cluster_repository.search_by_embedding(
                embedding, limit=3,
            )

            sessions = self.session_repository.search_by_embedding(
                embedding, limit=3,
            )

            topics = self.topic_repository.search_by_embedding(
                embedding, limit=3,
            )

            chunks = self.chunk_repository.search_chunks(
                embedding, limit=12,
            )

        context_parts: list[str] = []

        context_parts.append("# User Question")
        context_parts.append(question)

        # Related Concepts
        if related_entities:
            context_parts.append("# Related Concepts")
            context_parts.append(", ".join(sorted(related_entities)))

        # Topics
        if topics:
            context_parts.append("# Related Topics")
            for topic in topics:
                context_parts.append(f"""
Topic: {topic["title"]}, Summary: {topic["summary"]}""")
                
        # Sessions
        if sessions:
            context_parts.append("# Related Browsing Sessions")
            for session in sessions:
                context_parts.append(f"""
Session: {session["title"]}, Summary: {session["summary"]}""")
        
        # Memory Clusters
        if clusters:
            context_parts.append("# Related Memory Clusters")
            for cluster in clusters:
                context_parts.append(f"""
Topic: {cluster["title"]}, Summary: {cluster["summary"]}""")
        
        # Knowledge
        if chunks:
            context_parts.append("Relevant Knowledge")
            seen_tabs = set()

            filtered_chunks = []

            for chunk in chunks:
                tab_id = chunk["tab_id"]

                if tab_id in seen_tabs:
                    continue

                seen_tabs.add(tab_id)
                filtered_chunks.append(chunk)

                context_parts.append(f"""
Title: {chunk["title"]}, Content: {chunk["chunk_text"]}""")
        
        else:
            filtered_chunks = []
        
        context = "\n\n".join(context_parts)

        return ContextResult(
            context=context, chunks=filtered_chunks,
        )