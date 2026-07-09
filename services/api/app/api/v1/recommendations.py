from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.repositories.graph_repository import GraphRepository
from app.services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/api/v1/recommendations", tags=["Recommendations"],
)

@router.get("/topics")
def topics(db: Session = Depends(get_db)):
    service = RecommendationService(
        GraphRepository(db)
    )

    return service.trending_topics()

@router.get("/topic/{topic_id}")
def topic(
    topic_id: str, db: Session = Depends(get_db)
):
    service = RecommendationService(
        GraphRepository(db)
    )

    return service.recommend_tabs_for_topic(topic_id)

@router.get("/entity/{entity_id}")
def entity(
    entity_id: str, db: Session = Depends(get_db),
):
    service = RecommendationService(
        GraphRepository(db)
    )

    return service.recommend_tabs_for_entity(entity_id)