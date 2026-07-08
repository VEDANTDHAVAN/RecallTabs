from app.services.entity_extraction_service import EntityExtractionService
from app.services.graph_traversal_service import GraphTraversalService

from app.repositories.entity_repository import EntityRepository
from app.repositories.graph_traversal_repository import GraphTraversalRepository

class GraphContextService:
    def __init__(self, db):
        entity_repository = EntityRepository(db)
        traversal_repository = GraphTraversalRepository(db)

        self.entity_extractor = EntityExtractionService()
        self.graph = GraphTraversalService(
            entity_repository, traversal_repository,
        )

    def expand(self, question: str) -> list[str]:
        extracted = self.entity_extractor.extract(
            question, question
        )

        related = set()

        for entity in extracted:
            related.add(entity["name"])

            neighbours = self.graph.related_entities_multi_hop(entity["name"], depth=2)
            neighbours = sorted(neighbours, key=lambda x: x["weight"], reverse=True)[:10]

            for neighbour in neighbours:
                related.add(neighbour["name"])

        return list(related)