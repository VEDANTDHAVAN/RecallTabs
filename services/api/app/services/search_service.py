from app.services.embedding_service import EmbeddingService

class SearchService:
    def __init__(self, repository):
        self.repository = repository
        self.embedder = EmbeddingService()

    def search(self, query: str,):
        embedding = self.embedder.embed(query)

        return self.repository.semantic_search(embedding)