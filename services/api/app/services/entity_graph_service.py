from app.infrastructure.database.models.entity import Entity
from app.infrastructure.database.models.entity_alias import EntityAlias

from app.repositories.entity_repository import EntityRepository
from app.repositories.entity_alias_repository import EntityAliasRepository

from app.services.embedding_service import EmbeddingService

class EntityGraphService:
    SIMILARITY_THRESHOLD = 0.90

    def __init__(self, entity_repository: EntityRepository,
       alias_repository: EntityAliasRepository,
    ):
        self.entity_repository = entity_repository
        self.alias_repository = alias_repository
        self.embedder = EmbeddingService()

    def get_or_create(
        self, name: str, entity_type: str,
        summary: str | None = None,
    ) -> Entity:
        name = name.strip()

        if not name:
            raise ValueError("Entity name cannot be empty.")

        # Exact Match
        existing = self.entity_repository.get_by_name(name)

        if existing:
            existing.importance += 1
            return self.entity_repository.update(existing)
        
        # Alias Match
        alias = self.alias_repository.get(name)

        if alias:
            entity = self.entity_repository.get_by_id(alias.entity_id)

            if entity:
                entity.importance += 1
                return self.entity_repository.update(entity)

        # Semantic Match    
        embedding = self.embedder.embed(name)

        similar = self.entity_repository.search_by_embedding(
            embedding, limit=1,
        )

        if similar:
            best = similar[0]

            if best["score"] >= self.SIMILARITY_THRESHOLD:
                entity = self.entity_repository.get_by_id(best["id"])

                if entity:
                    # Avoid duplicate aliases
                    existing_alias = self.alias_repository.get(name)

                    if not existing_alias:
                        self.alias_repository.create(
                            EntityAlias(
                                entity_id=entity.id, alias=name,
                            )
                        )

                    entity.importance += 1

                    return self.entity_repository.update(entity)
        
        entity = Entity(
            name=name, entity_type=entity_type, summary=summary,
            embedding=embedding, importance=1.0,
        )

        return self.entity_repository.create(entity)