from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.schemas.search import SearchRequest, SearchResult

from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.tab_repository import TabRepository

from app.services.search_service import SearchService

from app.infrastructure.database.session import get_db

router = APIRouter(
    prefix="/search", tags=["search"],
)

@router.post("", response_model=list[SearchResult])
def search(
    payload: SearchRequest,
    db: Session = Depends(get_db),
):
    chunk_repository = TabChunkRepository(db)
    tab_repository = TabRepository(db)
    service = SearchService(chunk_repository, tab_repository)

    return service.search(payload.query)