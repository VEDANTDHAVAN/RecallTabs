from sqlalchemy import text
from sqlalchemy.orm import Session

from app.infrastructure.database.models.entity import Entity

class EntityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, entity: Entity) -> Entity:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def update(self, entity: Entity) -> Entity:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, entity_id: str) -> Entity | None:
        return (
            self.db.query(Entity).filter(Entity.id == entity_id).first()
        )
    
    def get_by_name(self, name: str) -> Entity | None:
        return (
            self.db.query(Entity).filter(Entity.name == name).first()
        )

    def search_by_embedding(self, embedding: list[float], limit: int = 5) -> list[dict]:
        query = text("""
        SELECT *, 1-(embedding <=> CAST(:embedding AS vector))
        AS score
        FROM entities
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
        """)

        rows = self.db.execute(query, {
            "embedding": str(embedding),
            "limit": limit,
        })

        return [
            dict(row._mapping) for row in rows
        ]

    def increment_importance(self, entity_id: str,
     amount: float = 1.0) -> Entity | None:
        entity = self.get_by_id(entity_id)

        if entity is None:
            return None

        entity.importance += amount

        return self.update(entity)