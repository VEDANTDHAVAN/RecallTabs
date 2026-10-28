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

    def get(self, conversation_id: str, user_id: str | None = None):
        q = self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        )
        if user_id is not None:
            q = q.filter(Conversation.user_id == user_id)
        return q.first()

    def list_by_user(self, user_id: str):
        return (
            self.db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).all()
        )

    def update_title(
        self, conversation_id: str, title: str, user_id: str | None = None,
    ):
        conversation = self.get(conversation_id, user_id=user_id)

        if not conversation:
            return None

        conversation.title = title

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def delete(self, conversation_id: str, user_id: str | None = None):
        conversation = self.get(conversation_id, user_id=user_id)

        if not conversation:
            return False

        self.db.delete(conversation)
        self.db.commit()

        return True
