from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.repositories.tab_repository import TabRepository
from app.repositories.tab_relationship_repository import TabRelationshipRepository
from app.services.knowledge_graph_service import KnowledgeGraphService

router = APIRouter(tags=["Knowledge Graph"])

@router.get("/tabs/{tab_id}/graph")
def graph(tab_id: str, db: Session = Depends(get_db)):
    service = (KnowledgeGraphService(
        TabRepository(db), 
        TabRelationshipRepository(db)
    ))

    return service.get_graph(tab_id)