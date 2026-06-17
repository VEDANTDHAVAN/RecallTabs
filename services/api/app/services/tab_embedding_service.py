from app.infrastructure.database.models.tab_chunk import TabChunk
from app.repositories.tab_chunk_repository import TabChunkRepository
from app.services.embedding_service import EmbeddingService
from app.services.text_chunker import TextChunker

class TabEmbeddingService:
    def __init__(self, repository):
        self.repository = repository
        self.chunker = TextChunker()
        self.embedder = EmbeddingService()

    def process(self, tab_id: str, content: str):
        if not content:
            return
        
        chunks = self.chunker.chunk(content)
        print(f"Chunks generated: {len(chunks)}")

        for chunk in chunks:
            embedding = self.embedder.embed(chunk)

            print(f"Embedding length: {len(embedding)}")

            entity = TabChunk(
                tab_id=tab_id, chunk_text=chunk, embedding=embedding,
            )

            self.repository.create(entity)