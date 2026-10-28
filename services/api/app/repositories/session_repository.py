from sqlalchemy.orm import Session
from sqlalchemy import text

from app.infrastructure.database.models.session import Session as RecallSession

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, session):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_all(self, user_id: str | None = None):
        q = self.db.query(RecallSession)
        if user_id is not None:
            q = q.filter(RecallSession.user_id == user_id)
        return q.all()

    def get_by_topic(self, topic: str, user_id: str | None = None):
        q = self.db.query(RecallSession).filter(
            RecallSession.topic == topic
        )
        if user_id is not None:
            q = q.filter(RecallSession.user_id == user_id)
        return q.first()

    def update(self, session):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def search_by_embedding(
        self, embedding, limit: int = 3, user_id: str | None = None,
    ):
        vector_str = "[" + ",".join(map(str, embedding)) + "]"

        sql = text("""
        SELECT id, title, summary,
               embedding <=> CAST(:embedding AS vector) AS distance
        FROM sessions
        WHERE embedding IS NOT NULL
          AND (:user_id IS NULL OR user_id = :user_id)
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
        """)

        result = self.db.execute(
            sql, {
                "embedding": vector_str,
                "limit": limit,
                "user_id": user_id,
            },
        )

        return [dict(row._mapping) for row in result]
