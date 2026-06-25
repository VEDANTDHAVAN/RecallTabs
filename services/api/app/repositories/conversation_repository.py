from sqlalchemy.orm import Session

from app.infrastructure.database.models.conversation import Conversation

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, conversation: Conversation):
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation
    
    def get(self, conversation_id: str):
        return (
            self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
        )
    
    def list_by_user(self, user_id: str):
        return (
            self.db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).all()
        )