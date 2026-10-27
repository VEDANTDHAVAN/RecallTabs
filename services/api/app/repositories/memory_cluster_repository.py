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
        vector_str = "[" + ",".join(map(str, embedding)) + "]"

        query = text("""
SELECT 
    id, title, summary,
    1 - (embedding <=> Entity.embedding.cosine_distance(embedding))
    AS score
FROM memory_clusters
ORDER BY
    embedding <=> Entity.embedding.cosine_distance(embedding)
LIMIT :limit
""")
        result = self.db.execute(
            query, {
                "embedding": vector_str,
                "limit": limit,
            }
        )

        return [
            dict(row._mapping)
            for row in result
        ]
    
    def search_by_embedding(
        self, embedding, limit: int = 3,
    ):
        vector_str = "[" + ",".join(map(str, embedding)) + "]"

        sql = text("""
SELECT id, title, summary, 
        embedding <=> Entity.embedding.cosine_distance(embedding)
            AS distance
FROM memory_clusters
WHERE embedding IS NOT NULL
ORDER BY embedding <=> Entity.embedding.cosine_distance(embedding)
LIMIT :limit
""")
        result = self.db.execute(
            sql, {
                "embedding": vector_str,
                "limit": limit,
            },
        )

        return [dict(row._mapping) for row in result]