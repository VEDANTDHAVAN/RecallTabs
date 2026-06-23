from sqlalchemy.orm import Session
from sqlalchemy import text

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
    
    def update(self, tab):
        self.db.add(tab)
        self.db.commit()
        self.db.refresh(tab)

        return tab
    
    def get_timeline(self, limit: int = 100):
        return (
            self.db.query(Tab).order_by(
                Tab.captured_at.desc()
            ).limit(limit).all()
        )
    
    def topic_statistics(self):
        query = text("""
SELECT topic,
COUNT(*) as count
FROM tabs
WHERE topic IS NOT NULL
AND topic <> ''
GROUP BY topic
ORDER BY count DESC
""")
        result = self.db.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]