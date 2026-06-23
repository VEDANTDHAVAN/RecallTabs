from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db

from app.repositories.session_repository import SessionRepository

router = APIRouter()

@router.get("/sessions")
def get_sessions(
    db: Session = Depends(get_db)
):
    repo = SessionRepository(db)

    return repo.get_all()