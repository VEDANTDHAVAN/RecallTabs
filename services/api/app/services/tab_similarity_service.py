from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.tab_relationship_repository import TabRelationshipRepository

class TabSimilarityService:
    def __init__(self, chunk_repository: TabChunkRepository,
        relationship_repository: TabRelationshipRepository,
    ):
        self.chunk_repository = chunk_repository
        self.relationship_repository = relationship_repository

    def build_relationships(
        self, tab_id: str, limit: int = 5,
    ):
        print("Building relationships for: ", tab_id)
        chunks = self.chunk_repository.get_chunks_by_tab_id(tab_id)
        print("Chunks:", len(chunks)) 

        if not chunks:
            return []
        
        created = []

        for chunk in chunks:
            similar_chunks = (
                self.chunk_repository.semantic_search(
                    chunk.embedding, limit=limit
                )
            )

            for item in similar_chunks:
                related_tab_id = item["tab_id"]
                score = item["score"]

                if related_tab_id == tab_id:
                    continue

                relation = (
                    self.relationship_repository.create(
                        source_id=tab_id, related_id=related_tab_id, score=score
                    )
                )

                created.append(relation)
        
        print(similar_chunks)

        return created