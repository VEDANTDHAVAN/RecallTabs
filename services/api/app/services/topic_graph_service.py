from app.infrastructure.database.models.topic import Topic

from app.repositories.topic_repository import TopicRepository
from app.services.embedding_service import EmbeddingService

from typing import cast, Optional

class TopicGraphService:
    SIMILARITY_THRESHOLD = 0.88

    def __init__(self, repository: TopicRepository):
        self.repository = repository
        self.embedder = EmbeddingService()

    def get_or_create(
        self, title: str, summary: str | None = None,
    ) -> Topic:
        title = title.strip()

        # Exact match first
        existing = self.repository.get_by_title(title)

        if existing is not None:
            return existing
        
        # Semantic search
        embedding = self.embedder.embed(title)

        candidates = self.repository.search_by_embedding(
            embedding, limit=1,
        )

        for candidate in candidates:
            if candidate["score"] >= self.SIMILARITY_THRESHOLD:
                topic = self.repository.get_by_id(candidate["id"])

                if topic:
                    return topic
                
        # Create new Topic
        topic = Topic(
            title=title, summary=summary,
            embedding=embedding, importance=1.0,
        )

        created = self.repository.create(topic)

        if created is None:
            raise RuntimeError("Failed to create topic.")
        
        return created
    
    def increment_importance(
        self, topic_id: str, amount: float = 1.0,
    ):
        self.repository.increment_importance(
            topic_id, amount,
        )