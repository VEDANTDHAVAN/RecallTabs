class KnowledgeGraphService:
    def __init__(
        self, tab_repository, relationship_repository,    
    ):
        self.tab_repository = tab_repository
        self.relationship_repository = (relationship_repository)

    def get_graph(self, tab_id: str):
        tab = self.tab_repository.get_by_id(tab_id)

        related = (self.relationship_repository.get_related(tab_id))

        return {
            "node": {
                "id": tab.id,
                "title": tab.title,
                "topic": tab.topic,
                "category": tab.category,
            },
            "neighbors": related,
        }