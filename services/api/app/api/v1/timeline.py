from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.repositories.tab_repository import TabRepository

from app.services.timeline_service import TimelineService

router = APIRouter()

@router.get("/timeline")
def timeline(db: Session = Depends(get_db)):
    service = TimelineService(TabRepository(db))

    return service.get_timeline()

@router.get("/timeline/topics")
def topics(db: Session = Depends(get_db)):
    service = TimelineService(TabRepository(db))

    return service.topic_stats()