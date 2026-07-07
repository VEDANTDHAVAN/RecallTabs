from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.models.tab import Tab

from app.repositories.tab_repository import TabRepository
from app.repositories.tab_chunk_repository import TabChunkRepository
from app.repositories.tab_relationship_repository import TabRelationshipRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.memory_cluster_repository import MemoryClusterRepository
from app.repositories.topic_repository import TopicRepository
from app.repositories.entity_repository import EntityRepository
from app.repositories.entity_alias_repository import EntityAliasRepository
from app.repositories.tab_entity_repository import TabEntityRepository

from app.services.tab_embedding_service import TabEmbeddingService
from app.services.tab_ai_service import TabAIService
from app.services.tab_similarity_service import TabSimilarityService
from app.services.session_detection_service import SessionDetectionService
from app.services.memory_cluster_service import MemoryClusterService
from app.services.memory_importance_service import MemoryImportanceService
from app.services.topic_graph_service import TopicGraphService
from app.services.entity_graph_service import EntityGraphService
from app.services.entity_extraction_service import EntityExtractionService
from app.services.tab_entity_service import TabEntityService

from app.schemas.tab_capture import TabCaptureRequest

class TabCaptureService:
    def __init__(self, db: Session):
        self.repository = TabRepository(db)
        self.chunk_repository = (TabChunkRepository(db))
        self.relationship_repository = (TabRelationshipRepository(db))
        self.entity_repository = EntityRepository(db)
        self.alias_repository = EntityAliasRepository(db)
        self.tab_entity_repository = TabEntityRepository(db)
        
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
        self.memory_service = MemoryImportanceService()
        self.entity_graph_service = EntityGraphService(
            self.entity_repository, self.alias_repository
        )
        self.entity_extraction_service = EntityExtractionService()
        self.tab_entity_service = TabEntityService(
            entity_service=self.entity_graph_service,
            extraction_service=self.entity_extraction_service,
            relation_repository=self.tab_entity_repository,
        )
        self.topic_graph = TopicGraphService(TopicRepository(db))
        self.db = db

    def capture(self, payload: TabCaptureRequest, user_id: str) -> Tab:
        url = str(payload.url).lower()

        ignored_domains = [
            "localhost", "127.0.0.1", "swagger",
            "chrome://", "chrome-extension://", "edge://", 
            "about:", "devtools://", "supabase.com/dashboard",
        ]

        is_searchable = not any(
            domain in url 
            for domain in ignored_domains
        )

        tab = Tab(
            user_id=user_id, title=payload.title,
            url=str(payload.url), content=payload.content,
            description=payload.description, favicon=payload.favicon,
            word_count=payload.word_count, is_searchable=is_searchable,
        )

        saved_tab = self.repository.create(tab)
        
        # Ignore indexing for non-searchable pages
        if not saved_tab.is_searchable:
            return saved_tab
        
        if not saved_tab.content:
            return saved_tab

        # Generate embeddings
        self.embedding_service.process(
            tab_id=saved_tab.id, content=saved_tab.content,
        )
        # Relationships
        self.similarity_service.build_relationships(saved_tab.id)
        # AI Metadata 
        analysis = self.ai_service.analyze(saved_tab.content or "")

        topic = self.topic_graph.get_or_create(
            title=analysis["topic"], summary=analysis["summary"],
        )

        saved_tab.summary = analysis["summary"]
        saved_tab.keywords = analysis["keywords"]
        saved_tab.category = analysis["category"]

        saved_tab.topic_id = topic.id 

        saved_tab.open_count += 1
        saved_tab.last_opened_at = datetime.utcnow()

        self.memory_service.calculate(saved_tab)

        self.repository.update(saved_tab)

        self.tab_entity_service.process(
            tab_id=saved_tab.id, title=saved_tab.title,
            content=saved_tab.content,
        )
        # Session    
        session = self.session_service.assign_session(saved_tab)
        if session:
            self.cluster_service.assign_cluster(session)

        return saved_tab