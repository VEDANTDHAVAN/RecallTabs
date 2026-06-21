from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.repositories.tab_relationship_repository import TabRelationshipRepository

router = APIRouter()

@router.get("/tabs/{tab_id}/related")
def related(
    tab_id: str, db: Session = Depends(get_db),
):
    repo = TabRelationshipRepository(db)
    
    return repo.get_related(tab_id)