from app.infrastructure.database.models.memory_cluster import MemoryCluster

from app.services.embedding_service import EmbeddingService

class MemoryClusterService:
    def __init__(
        self, cluster_repository,
        session_repository,
    ):
        self.cluster_repository = cluster_repository
        self.session_repository = session_repository
        self.embedder = EmbeddingService()

    def assign_cluster(
        self, session, threshold=0.70,
    ):
        embedding = (
            self.embedder.embed(session.topic)
        )

        matches = (
            self.cluster_repository.semantic_search(
                embedding, limit=1
            )
        )
        print(matches)

        if matches:
            best = matches[0]

            if best["score"] > threshold:
                session.cluster_id = best["id"]

                self.session_repository.update(session)

                return best
            
        cluster = MemoryCluster(
            title=session.topic, embedding=embedding,
            summary = session.summary,
        )

        saved = (
            self.cluster_repository.create(cluster)
        )

        session.cluster_id = saved.id

        self.session_repository.update(session)

        return saved