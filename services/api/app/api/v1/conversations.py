from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

from app.services.conversation_management_service import ConversationManagementService

from app.schemas.conversation import ConversationUpdate

from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

@router.post("")
def create_conversation(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.create(user_id=current_user.id)

@router.get("")
def list_conversations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.list(current_user.id)

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.get(conversation_id, user_id=current_user.id)

@router.get("/{conversation_id}/messages")
def get_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repository = MessageRepository(db)

    return repository.get_messages(conversation_id, user_id=current_user.id)

@router.patch("/{conversation_id}")
def rename_conversation(
    conversation_id: str,
    payload: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return service.rename(
        conversation_id, payload.title, user_id=current_user.id,
    )

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ConversationManagementService(
        ConversationRepository(db)
    )

    return {
        "deleted": service.delete(conversation_id, user_id=current_user.id)
    }
