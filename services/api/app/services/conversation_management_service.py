from app.infrastructure.database.models.conversation import Conversation

class ConversationManagementService:
    def __init__(self, repository):
        self.repository = repository

    def create(
        self, user_id: str, title: str | None = None
    ):
        conversation = Conversation(
            user_id=user_id, title=title,
        )

        return self.repository.create(conversation)

    def list(self, user_id: str):
        return self.repository.list_by_user(user_id)

    def get(self, conversation_id: str, user_id: str | None = None):
        return self.repository.get(conversation_id, user_id=user_id)

    def rename(self, conversation_id: str, title: str, user_id: str | None = None):
        return self.repository.update_title(conversation_id, title, user_id=user_id)

    def delete(self, conversation_id: str, user_id: str | None = None):
        return self.repository.delete(conversation_id, user_id=user_id)
