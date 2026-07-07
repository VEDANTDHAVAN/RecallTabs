from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.repositories.knowledge_graph_repository import KnowledgeGraphRepository

from app.services.knowledge_graph_service import KnowledgeGraphService

router = APIRouter(tags=["Knowledge Graph"], prefix="/knowledge")

@router.get("/{entity}")
def get_entity(
    entity: str, 
    db: Session = Depends(get_db),
):
    service = KnowledgeGraphService(
        KnowledgeGraphRepository(db)
    )

    return service.entity_graph(entity)