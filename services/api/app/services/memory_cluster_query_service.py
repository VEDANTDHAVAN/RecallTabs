class MemoryClusterQueryService:
    def __init__(self, repository):
        self.repository = repository

    def get_clusters(self):
        clusters = self.repository.get_all()

        return [
            {
                "id": c.id,
                "title": c.title,
                "summary": c.summary,
            } for c in clusters
        ]