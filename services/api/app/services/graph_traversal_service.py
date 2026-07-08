from collections import deque

from app.repositories.entity_repository import EntityRepository
from app.repositories.graph_traversal_repository import GraphTraversalRepository

class GraphTraversalService:
    def __init__(
        self, entity_repository: EntityRepository,
        traversal_repository: GraphTraversalRepository,
    ):
        self.entity_repository = entity_repository
        self.traversal_repository = traversal_repository

    def related_entities(self, name: str):
        entity = self.entity_repository.get_by_name(name)

        if entity is None:
            return []
        
        return self.traversal_repository.neighbors(entity.id)
    
    def related_entities_multi_hop(
        self, name: str, depth: int = 2,
    ):
        root = self.entity_repository.get_by_name(name)

        if root is None:
            return []
        
        queue = deque()

        queue.append((root.id, 0))

        visited = {root.id}

        results = []

        while queue:
            entity_id, level = queue.popleft()

            if level >= depth:
                continue

            neighbours = self.traversal_repository.neighbors(
                entity_id, limit=20,
            )

            for neighbour in neighbours:
                if neighbour["id"] in visited:
                    continue

                visited.add(neighbour["id"])

                results.append(neighbour)

                queue.append((
                    neighbour["id"], level + 1,
                ))

        return results