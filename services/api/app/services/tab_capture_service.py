from sqlalchemy.orm import Session

from app.infrastructure.database.models.tab import Tab
from app.repositories.tab_repository import TabRepository
from app.schemas.tab_capture import TabCaptureRequest
from app.repositories.tab_chunk_repository import TabChunkRepository
from app.services.tab_embedding_service import TabEmbeddingService
from app.services.tab_ai_service import TabAIService

class TabCaptureService:
    def __init__(self, db: Session):
        self.repository = TabRepository(db)
        self.chunk_repository = (TabChunkRepository(db))
        self.embedding_service = (TabEmbeddingService(self.chunk_repository))
        self.ai_service = TabAIService()
        self.db = db

    def capture(self, payload: TabCaptureRequest, user_id: str) -> Tab:
        tab = Tab(
            user_id=user_id, title=payload.title, url=str(payload.url), content=payload.content, 
            description=payload.description, favicon=payload.favicon, word_count=payload.word_count,
        )

        saved_tab = self.repository.create(tab)

        # Generate embeddings only if content exists
        if saved_tab.content:
            self.embedding_service.process(
                tab_id=saved_tab.id, content=saved_tab.content,
            )

            analysis = self.ai_service.analyze(saved_tab.content or "")

            saved_tab.summary = analysis["summary"]
            saved_tab.keywords = analysis["keywords"]
            saved_tab.topic = analysis["topic"]
            saved_tab.category = analysis["category"]
            
            self.db.commit()
            self.db.refresh(saved_tab)

        return saved_tab