from app.services.embedding_service import EmbeddingService

class ContextSelectionService:
    def __init__(
        self, chunk_repository,
        session_repository, cluster_repository,
    ):
        self.chunk_repository = chunk_repository
        self.session_repository = session_repository
        self.cluster_repository = cluster_repository
        self.embedder = EmbeddingService()
        
    def build_context(self, question: str) -> str:
        embedding = self.embedder.embed(question)

        clusters = self.cluster_repository.search_by_embedding(
            embedding, limit=3,
        )

        sessions = self.session_repository.search_by_embedding(
            embedding, limit=3,
        )

        chunks = self.chunk_repository.search_chunks(
            embedding, limit=12,
        )

        context_parts = []

        # Memory Clusters
        if clusters:
            context_parts.append("# Related Memory Clusters")

            for cluster in clusters:
                context_parts.append(f"""Topic: {cluster['title']}
Summary: {cluster['summary']}
""")
            
        # Sessions
        if sessions:
            context_parts.append("# Related Browsing Sessions")
            for session in sessions:
                context_parts.append(f"""
Session: {session['title']} \nSummary: {session['summary']}""")
                    
        # Chunks
        if chunks:
            context_parts.append("# Relevant Knowledge")
            for chunk in chunks:
                context_parts.append(chunk["chunk_text"])

        return "\n\n".join(context_parts)