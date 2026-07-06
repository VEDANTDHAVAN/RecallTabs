from sqlalchemy import text
from sqlalchemy.orm import Session

from app.infrastructure.database.models.topic import Topic
from typing import Optional

class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, topic: Topic) -> Topic:
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def update(self, topic: Topic) -> Topic:
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def get_by_title(self, title: str) -> Optional[Topic]:
        return (
            self.db.query(Topic)
            .filter(Topic.title == title)
            .first()
        )

    def get_by_id(self, topic_id: str) -> Optional[Topic]:
        return (
            self.db.query(Topic)
            .filter(Topic.id == topic_id)
            .first()
        )

    def search_by_embedding(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:
        query = text("""
SELECT
    *,
    1-(embedding <=> CAST(:embedding AS vector))
    AS score
FROM topics
WHERE embedding IS NOT NULL
ORDER BY embedding <=> CAST(:embedding AS vector)
LIMIT :limit
""")

        rows = self.db.execute(
            query,
            {
                "embedding": str(embedding),
                "limit": limit,
            },
        )

        return [
            dict(row._mapping)
            for row in rows
        ]
    
    def increment_importance(
        self, topic_id: str, amount: float = 1.0,
    ) -> Topic | None:
        topic = self.get_by_id(topic_id)

        if topic:
            topic.importance += amount
            return self.update(topic)
        
        return None