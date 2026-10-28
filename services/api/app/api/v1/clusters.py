from fastapi import APIRouter, Depends

from app.infrastructure.database.session import get_db
from app.auth.dependencies import get_current_user

from sqlalchemy.orm import Session

from app.repositories.memory_cluster_repository import MemoryClusterRepository
from app.services.memory_cluster_query_service import MemoryClusterQueryService

router = APIRouter()

@router.get("/clusters")
def get_clusters(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = MemoryClusterQueryService(
        MemoryClusterRepository(db)
    )

    clusters = service.get_clusters()
    # filter by user
    repo = MemoryClusterRepository(db)
    user_clusters = repo.get_all(user_id=current_user.id)
    user_ids = {c.id for c in user_clusters}
    return [c for c in clusters if c["id"] in user_ids]
