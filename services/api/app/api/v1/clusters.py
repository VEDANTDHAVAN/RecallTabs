from fastapi import APIRouter, Depends

from app.infrastructure.database.session import get_db

from sqlalchemy.orm import Session

from app.repositories.memory_cluster_repository import MemoryClusterRepository
from app.services.memory_cluster_query_service import MemoryClusterQueryService

router = APIRouter()

@router.get("/clusters")
def get_clusters(db: Session = Depends(get_db)):
    service = MemoryClusterQueryService(
        MemoryClusterRepository(db)
    )

    return service.get_clusters()