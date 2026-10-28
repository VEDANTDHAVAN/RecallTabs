from collections import defaultdict

from app.services.embedding_service import EmbeddingService
from app.services.search_intent_service import SearchIntentService, SearchIntent

from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.tab_repository import TabRepository

class SearchService:
    def __init__(self, chunk_repository: TabChunkRepository, tab_repository: TabRepository):
        self.chunk_repository = chunk_repository
        self.tab_repository = tab_repository
        self.embedder = EmbeddingService()
        self.intent = SearchIntentService()

    async def search(self, query: str, user_id: str):
        embedding = await self.embedder.embed(query)

        semantic = self.chunk_repository.semantic_search(
            embedding, limit=15, user_id=user_id,
        )

        keyword = self.tab_repository.keyword_search(
                        user_id, query, limit=15,
                    )

        results = self.rank_results(
            semantic, keyword,
        )

        intent = self.intent.detect(query)

        if intent == SearchIntent.KEYWORD:
            keyword = self.tab_repository.keyword_search(user_id, query)

            return keyword

        elif intent == SearchIntent.SEMANTIC:
            semantic = self.chunk_repository.semantic_search(embedding, user_id=user_id)

            return semantic

        elif intent == SearchIntent.HYBRID:
            semantic = self.chunk_repository.semantic_search(embedding, user_id=user_id)
            keyword = self.tab_repository.keyword_search(user_id, query)

            return self.rank_results(semantic, keyword)

        elif intent == SearchIntent.DOMAIN:
            return self.tab_repository.domain_search(user_id, query)

        return results

    def rank_results(self, semantic, keyword):
        # Reciprocal Rank Fusion (RRF)
        K = 60
        scores = defaultdict(float)
        objects = {}

        SEMANTIC_WEIGHT = 0.7
        KEYWORD_WEIGHT = 0.3

        for rank, item in enumerate(semantic):
            scores[item["tab_id"]] += SEMANTIC_WEIGHT / (K + rank + 1)
            objects[item["tab_id"]] = item

        for rank, item in enumerate(keyword):
            scores[item["tab_id"]] += KEYWORD_WEIGHT / (K + rank + 1)
            objects[item["tab_id"]] = item

        ranked = sorted(
            scores.items(), reverse=True,
            key=lambda x: x[1],
        )

        results = []

        for tab_id, score in ranked:
            tab = objects[tab_id]
            tab["score"] = round(score * 1000, 2)
            results.append(tab)

        return results
