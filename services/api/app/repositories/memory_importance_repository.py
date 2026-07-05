from sqlalchemy.orm import Session
from app.infrastructure.database.models.tab import Tab

class MemoryImportanceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, tab_id: str):
        return (
            self.db.query(Tab).filter(Tab.id == tab_id).first()
        )
    
    def save(self, tab: Tab):
        self.db.add(tab)
        self.db.commit()
        self.db.refresh(tab)

        return tab
    
    def list_all(self):
        return self.db.query(Tab).all()