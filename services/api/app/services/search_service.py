from app.services.embedding_service import EmbeddingService
from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.tab_repository import TabRepository

class SearchService:
    def __init__(self, chunk_repository: TabChunkRepository, tab_repository: TabRepository):
        self.chunk_repository = chunk_repository
        self.tab_repository = tab_repository
        self.embedder = EmbeddingService()

    def search(self, query: str,):
        embedding = self.embedder.embed(query)

        return self.chunk_repository.semantic_search(embedding, limit=10)