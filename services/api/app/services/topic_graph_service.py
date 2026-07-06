from app.infrastructure.database.models.topic import Topic

from app.repositories.topic_repository import TopicRepository
from app.services.embedding_service import EmbeddingService

from typing import cast

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
        
        embedding = self.embedder.embed(title)

        similar = self.repository.search_by_embedding(
            embedding, limit=1,
        )

        if similar:
            best = similar[0]

            if best["score"] >= self.SIMILARITY_THRESHOLD:
                topic = self.repository.get_by_id(best["id"])

                if topic is not None:
                    return topic
                
        topic = Topic(
            title=title, summary=summary,
            embedding=embedding, importance=1.0,
        )

        created = self.repository.create(topic)

        return cast(Topic, created)