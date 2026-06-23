from sqlalchemy.orm import Session

from app.infrastructure.database.models.tab import Tab

from app.repositories.tab_repository import TabRepository
from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.tab_relationship_repository import TabRelationshipRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.memory_cluster_repository import MemoryClusterRepository

from app.services.tab_embedding_service import TabEmbeddingService
from app.services.tab_ai_service import TabAIService
from app.services.tab_similarity_service import TabSimilarityService
from app.services.session_detection_service import SessionDetectionService
from app.services.memory_cluster_service import MemoryClusterService

from app.schemas.tab_capture import TabCaptureRequest

class TabCaptureService:
    def __init__(self, db: Session):
        self.repository = TabRepository(db)
        self.chunk_repository = (TabChunkRepository(db))
        self.relationship_repository = (TabRelationshipRepository(db))
        self.embedding_service = (TabEmbeddingService(self.chunk_repository))
        self.ai_service = TabAIService()
        self.similarity_service = (TabSimilarityService(
            self.chunk_repository, self.relationship_repository,
        ))
        self.session_service = SessionDetectionService(
            SessionRepository(db), self.repository,
        )
        self.cluster_service = MemoryClusterService(
            MemoryClusterRepository(db), SessionRepository(db)
        )
        self.db = db

    def capture(self, payload: TabCaptureRequest, user_id: str) -> Tab:
        tab = Tab(
            user_id=user_id, title=payload.title, url=str(payload.url), content=payload.content, 
            description=payload.description, favicon=payload.favicon, word_count=payload.word_count,
        )

        ignored_domains = ["localhost", "swagger"]

        url = str(payload.url).lower()

        if any(x in url for x in ignored_domains):
            return tab

        saved_tab = self.repository.create(tab)

        # Generate embeddings only if content exists
        if saved_tab.content:
            self.embedding_service.process(
                tab_id=saved_tab.id, content=saved_tab.content,
            )

            self.similarity_service.build_relationships(saved_tab.id)

            analysis = self.ai_service.analyze(saved_tab.content or "")

            saved_tab.summary = analysis["summary"]
            saved_tab.keywords = analysis["keywords"]
            saved_tab.topic = analysis["topic"]
            saved_tab.category = analysis["category"]

            self.repository.update(saved_tab)
            session = self.session_service.assign_session(saved_tab)
            if session:
                self.cluster_service.assign_cluster(session)

        return saved_tab