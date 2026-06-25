from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest

from app.infrastructure.database.session import get_db

from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.message_repository import MessageRepository

from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/chat", tags=["Chat"],)

@router.post("/{conversation_id}")
def chat(
    conversation_id: str, payload: ChatRequest,
    db: Session = Depends(get_db),
):
    service = ConversationService(
        TabChunkRepository(db), MessageRepository(db)
    )

    return service.chat(conversation_id, payload.question)