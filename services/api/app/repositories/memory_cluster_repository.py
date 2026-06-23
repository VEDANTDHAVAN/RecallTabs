from sqlalchemy.orm import Session
from sqlalchemy import text

from app.infrastructure.database.models.memory_cluster import MemoryCluster

class MemoryClusterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cluster):
        self.db.add(cluster)
        self.db.commit()
        self.db.refresh(cluster)

        return cluster
    
    def get_all(self):
        return (
            self.db.query(MemoryCluster).all()
        )
    
    def update(self, cluster):
        self.db.add(cluster)
        self.db.commit()
        self.db.refresh(cluster)

        return cluster
    
    def get_by_id(self, cluster_id: str):
        return (
            self.db.query(MemoryCluster).filter(
                MemoryCluster.id == cluster_id
            ).first()
        )
    

    def semantic_search(
        self, embedding: list[float],
        limit: int = 1,
    ):
        query = text("""
SELECT 
    id, title, summary,
    1 - (embedding <=> CAST(:embedding AS vector))
    AS score
FROM memory_clusters
ORDER BY
    embedding <=> CAST(:embedding AS vector)
LIMIT :limit
""")
        result = self.db.execute(
            query, {
                "embedding": str(embedding),
                "limit": limit,
            }
        )

        return [
            dict(row._mapping)
            for row in result
        ]