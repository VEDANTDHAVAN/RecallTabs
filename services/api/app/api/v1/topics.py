from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.repositories.topic_repository import TopicRepository
from app.services.topic_service import TopicService

router = APIRouter(tags=["Topics"])

@router.get("/topics")
def topics(
    db: Session = Depends(get_db)
):
    repo = TopicRepository(db)

    service = TopicService(repo)

    return service.get_topics()

@router.get("/topics/{topic}/tabs")
def topic_tabs(
    topic: str, db: Session = Depends(get_db)
):
    repo = TopicRepository(db)
    service = TopicService(repo)

    return service.get_topic_tabs(topic)