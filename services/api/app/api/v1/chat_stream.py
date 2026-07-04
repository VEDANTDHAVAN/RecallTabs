from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.schemas.chat import ChatRequest

from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.memory_cluster_repository import MemoryClusterRepository

from app.services.conversation_service import ConversationService

router = APIRouter(
    prefix="/chat-stream", tags=["Streaming Chat"],
)

@router.post("/{conversation_id}")
def stream_chat(
    conversation_id: str, payload: ChatRequest,
    db: Session = Depends(get_db),
):
    service = ConversationService(
        TabChunkRepository(db), MessageRepository(db),
        SessionRepository(db), MemoryClusterRepository(db),
    )

    return StreamingResponse(
        service.stream_chat(
            question=payload.question,
            conversation_id=conversation_id,
        ),
        media_type="text/plain",
    )
