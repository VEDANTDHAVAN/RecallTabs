from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.repositories.graph_repository import GraphRepository

from app.services.graph_service import GraphService

router = APIRouter(
    prefix="/api/v1/graph", tags=["Graph"],
)

@router.get("/topics")
def topics(db: Session = Depends(get_db)):
    service = GraphService(GraphRepository(db))

    return service.get_topics()

@router.get("/topic/{topic_id}")
def topic(topic_id: str, db: Session = Depends(get_db)):
    service = GraphService(GraphRepository(db))

    return service.get_topic_graph(topic_id)

@router.get("/entity/{entity_id}")
def entity(
    entity_id: str, db: Session = Depends(get_db),
):
    service = GraphService(GraphRepository(db))

    return service.get_entity_graph(entity_id)