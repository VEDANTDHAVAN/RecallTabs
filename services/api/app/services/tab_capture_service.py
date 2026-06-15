from sqlalchemy.orm import Session

from app.infrastructure.database.models.tab import Tab
from app.repositories.tab_repository import TabRepository
from app.schemas.tab_capture import TabCaptureRequest

class TabCaptureService:
    def __init__(self, db: Session):
        self.repository = TabRepository(db)

    def capture(self, payload: TabCaptureRequest, user_id: str) -> Tab:
        tab = Tab(
            user_id=user_id, title=payload.title, url=str(payload.url), content=None
        )

        return self.repository.create(tab)