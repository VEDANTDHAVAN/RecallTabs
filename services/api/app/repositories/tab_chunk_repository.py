from sqlalchemy.orm import Session

from app.infrastructure.database.models.tab_chunk import TabChunk

class TabChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tab_chunk: TabChunk):
        self.db.add(tab_chunk)
        self.db.commit()
        self.db.refresh(tab_chunk)

        return tab_chunk