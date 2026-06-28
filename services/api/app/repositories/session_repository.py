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
    
    def get_all(self):
        return (
            self.db.query(RecallSession).all()
        )
    
    def get_by_topic(self, topic: str):
        return (
            self.db.query(RecallSession).filter(
                RecallSession.topic == topic
            ).first()
        )
    
    def update(self, session):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session
    
    def search_by_embedding(
        self, embedding, limit: int = 3
    ):
        sql = text("""
SELECT id, title, summary, embedding <=> CAST(:embedding AS vector)
       AS distance
FROM sessions
WHERE embedding IS NOT NULL
ORDER BY embedding <=> CAST(:embedding AS vector)
LIMIT :limit 
""")
        
        result = self.db.execute(
            sql, {
                "embedding": embedding,
                "limit": limit,
            },
        )

        return [dict(row._mapping) for row in result]