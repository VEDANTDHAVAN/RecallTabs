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

    def get_all(self, user_id: str | None = None):
        q = self.db.query(MemoryCluster)
        if user_id is not None:
            q = q.filter(MemoryCluster.user_id == user_id)
        return q.all()

    def update(self, cluster):
        self.db.add(cluster)
        self.db.commit()
        self.db.refresh(cluster)

        return cluster

    def get_by_id(self, cluster_id: str, user_id: str | None = None):
        q = self.db.query(MemoryCluster).filter(
            MemoryCluster.id == cluster_id
        )
        if user_id is not None:
            q = q.filter(MemoryCluster.user_id == user_id)
        return q.first()

    def semantic_search(
        self, embedding: list[float],
        limit: int = 1, user_id: str | None = None,
    ):
        vector_str = "[" + ",".join(map(str, embedding)) + "]"

        query = text("""
SELECT
    id, title, summary,
    1 - (embedding <=> CAST(:embedding AS vector)) AS score
FROM memory_clusters
WHERE (:user_id IS NULL OR user_id = :user_id)
ORDER BY
    embedding <=> CAST(:embedding AS vector)
LIMIT :limit
""")
        result = self.db.execute(
            query, {
                "embedding": vector_str,
                "limit": limit,
                "user_id": user_id,
            }
        )

        return [
            dict(row._mapping)
            for row in result
        ]

    def search_by_embedding(
        self, embedding, limit: int = 3, user_id: str | None = None,
    ):
        vector_str = "[" + ",".join(map(str, embedding)) + "]"

        sql = text("""
SELECT id, title, summary,
        embedding <=> CAST(:embedding AS vector) AS distance
FROM memory_clusters
WHERE embedding IS NOT NULL
  AND (:user_id IS NULL OR user_id = :user_id)
ORDER BY embedding <=> CAST(:embedding AS vector)
LIMIT :limit
""")
        result = self.db.execute(
            sql, {
                "embedding": vector_str,
                "limit": limit,
                "user_id": user_id,
            },
        )

        return [dict(row._mapping) for row in result]
