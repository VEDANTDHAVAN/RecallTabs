from datetime import datetime

from app.infrastructure.database.models.entity import Entity
from app.infrastructure.database.models.entity_alias import EntityAlias

from app.repositories.entity_repository import EntityRepository
from app.repositories.entity_alias_repository import EntityAliasRepository

from app.services.embedding_service import EmbeddingService

class EntityGraphService:
    SIMILARITY_THRESHOLD = 0.90

    def __init__(self, entity_repository: EntityRepository,
       alias_repository: EntityAliasRepository,
       embedding_service: EmbeddingService,
    ):
        self.entity_repository = entity_repository
        self.alias_repository = alias_repository
        self.embedding_service = embedding_service

    @staticmethod
    def normalize(name: str) -> str:
        return " ".join(name.strip().split())

    async def get_or_create(
        self, name: str, entity_type: str,
        description: str | None = None, confidence: float = 1.0,
    ) -> Entity:
        name = self.normalize(name)
        
        if not name:
            raise ValueError("Entity name cannot be empty.")

        # Exact Match
        existing = self.entity_repository.get_by_name(name)

        if existing:
            existing.importance += 1
            existing.mention_count += 1
            existing.last_seen_at = datetime.utcnow()

            return self.entity_repository.update(existing)
        
        # Alias Match
        alias = self.alias_repository.get(name)

        if alias:
            entity = self.entity_repository.get_by_id(alias.entity_id)

            if entity:
                entity.mention_count += 1
                entity.importance += 1
                entity.last_seen_at = datetime.utcnow()

                return self.entity_repository.update(entity)

        # Semantic Match    
        embedding = await self.embedding_service.embed(name)

        candidates = self.entity_repository.search_by_embedding(
            embedding, limit=5,
        )

        for candidate in candidates:
            if (candidate["score"] >= self.SIMILARITY_THRESHOLD and candidate["entity_type"] == entity_type):
                entity = self.entity_repository.get_by_id(candidate["id"])

                if entity:
                    if self.alias_repository.get(name) is None:
                        self.alias_repository.create(
                            EntityAlias(
                                entity_id=entity.id, alias=name,
                            )
                        )

                    entity.mention_count += 1
                    entity.importance += 1
                    entity.last_seen_at = datetime.utcnow()

                    return self.entity_repository.update(entity)

        # Create New Entity
        entity = Entity(
            name=name, entity_type=entity_type,
            description=description, embedding=embedding,
            confidence=confidence, mention_count=1,
            importance=1.0, last_seen_at=datetime.utcnow(),
        )

        return self.entity_repository.create(entity)