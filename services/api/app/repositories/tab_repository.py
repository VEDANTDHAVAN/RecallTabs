from sqlalchemy.orm import Session

from app.infrastructure.database.models.tab import Tab

class TabRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tab: Tab) -> Tab:
        self.db.add(tab)
        self.db.commit()
        self.db.refresh(tab)

        return tab
    
    def get_by_id(self, tab_id: str) -> Tab | None:
        return (
            self.db.query(Tab).filter(Tab.id == tab_id).first()
        )
    
    def list_by_user(
        self, user_id: str,
    ) -> list[Tab]:
        return (
            self.db.query(Tab).filter(Tab.user_id == user_id).all()
        )