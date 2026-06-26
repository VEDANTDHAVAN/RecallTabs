from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

from app.services.conversation_management_service import ConversationManagementService

from app.schemas.conversation import ConversationUpdate

def get_current_user_id():
    return "125657ed-f496-4735-8391-696b96be49c8"

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

@router.post("")
def create_conversation(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.create(user_id=user_id)

@router.get("")
def list_conversations(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.list(user_id)

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.get(conversation_id)

@router.get("/{conversation_id}/messages")
def get_messages(
    conversation_id: str, 
    db: Session = Depends(get_db)
):
    repository = MessageRepository(db)

    return repository.get_messages(conversation_id)

@router.patch("/{conversation_id}")
def rename_conversation(
    conversation_id: str,
    payload: ConversationUpdate,
    db: Session = Depends(get_db),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.rename(
        conversation_id, payload.title
    )

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return {
        "deleted": service.delete(conversation_id)
    }