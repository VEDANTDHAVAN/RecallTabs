from itertools import combinations

from app.infrastructure.database.models.entity_relationship import EntityRelationship

class EntityRelationshipService:
    def __init__(self, repository):
        self.repository = repository

    def build(self, entities):
        ids = sorted({
            entity.id for entity in entities
        })

        for a, b in combinations(ids, 2):
            relation = self.repository.get(a, b)

            if relation:
                relation.weight += 1
                self.repository.update(relation)

                continue

            self.repository.create(
                EntityRelationship(
                    entity_a_id=a,
                    entity_b_id=b, weight=1,
                )
            )