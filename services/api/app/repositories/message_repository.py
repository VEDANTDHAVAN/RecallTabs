from sqlalchemy.orm import Session

from app.infrastructure.database.models.message import Message

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, message: Message):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message
    
    def get_messages(self, conversation_id: str):
        return (
            self.db.query(Message).filter(
                Message.conversation_id == conversation_id
            ).all()
        )