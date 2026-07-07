from app.repositories.knowledge_graph_repository import KnowledgeGraphRepository

class KnowledgeGraphService:
    def __init__(
        self, repository: KnowledgeGraphRepository,    
    ):
        self.repository = repository

    def entity_graph(self, entity: str):
        rows = self.repository.get_entity_graph(entity)

        if not rows:
            return None
        
        graph = {
            "entity": rows[0]["name"],
            "type": rows[0]["entity_type"],
            "tabs": [],
        }

        seen = set()

        for row in rows:
            if row["tab_id"] in seen:
                continue

            seen.add(row["tab_id"])

            graph["tabs"].append({
                "title": row["title"],
                "url": row["url"],
                "topic": row["topic"],
                "session": row["session"],
                "cluster": row["cluster"],
            })

        return graph