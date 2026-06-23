from sqlalchemy.orm import Session

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