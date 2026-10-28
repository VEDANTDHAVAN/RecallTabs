from sqlalchemy.orm import Session

from app.infrastructure.database.models.message import Message
from app.infrastructure.database.models.conversation import Conversation

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, message: Message):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_messages(self, conversation_id: str, user_id: str | None = None):
        q = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        )
        if user_id is not None:
            q = q.join(Conversation, Conversation.id == Message.conversation_id).filter(
                Conversation.user_id == user_id
            )
        return q.all()

    def update(self, message: Message):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message
