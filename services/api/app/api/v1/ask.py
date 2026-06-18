from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.schemas.ask import AskRequest, AskResponse

from app.repositories.tab_chunk_repository import TabChunkRepository

from app.services.ask_service import AskService

router = APIRouter(prefix="/ask", tags=["Ask"],)

@router.post("", response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db),):
    repository = TabChunkRepository(db)
    service = AskService(repository)

    return service.ask(payload.question)