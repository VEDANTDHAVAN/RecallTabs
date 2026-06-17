from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.search import SearchRequest, SearchResult

from app.repositories.tab_chunk_repository import TabChunkRepository

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
    repository = TabChunkRepository(db)
    service = SearchService(repository)

    return service.search(payload.query)