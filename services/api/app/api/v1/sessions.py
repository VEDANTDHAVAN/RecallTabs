from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.auth.dependencies import get_current_user

from app.repositories.session_repository import SessionRepository

router = APIRouter()

@router.get("/sessions")
def get_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = SessionRepository(db)

    return repo.get_all(user_id=current_user.id)
