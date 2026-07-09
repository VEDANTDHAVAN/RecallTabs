class ContextRankingService:
    def score(self, chunk):
        score = chunk["score"]

        score += chunk.get("importance", 0) * 0.15
        score += chunk.get("chat_reference_count", 0) * 0.05
        score += chunk.get("visit_count", 0) * 0.02

        return score
    
    def rank(self, chunks):
        return sorted(
            chunks, key=self.score, reverse=True,
        )