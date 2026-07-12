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
SELECT tp.title AS topic,
COUNT(*) as count
FROM tabs t
LEFT JOIN topics tp ON tp.id = t.topic_id
WHERE tp.title IS NOT NULL
AND tp.title <> ''
GROUP BY tp.title
ORDER BY count DESC
""")
        result = self.db.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]
    
    def keyword_search(
        self, query: str, limit: int = 10,
    ):
        sql = text("""
SELECT t.id, t.title, t.url, t.favicon,
    t.summary, tp.title AS topic, ts_rank(
        to_tsvector(
            'english', 
            coalesce(t.title, '') || ' ' ||
            coalesce(t.summary, '') || ' ' ||
            coalesce(t.content, '')
        ),
        plainto_tsquery('english', :query)
    ) AS score
FROM tabs t
LEFT JOIN topics tp ON tp.id = t.topic_id
WHERE t.is_searchable = TRUE
AND
    to_tsvector(
     'english', coalesce(t.title, '') || ' ' ||
     coalesce(t.summary, '') || ' ' ||
     coalesce(t.content, '')
    )
    @@ plainto_tsquery('english', :query)
ORDER BY score DESC
LIMIT :limit
""")
        rows = self.db.execute(
            sql, {
                "query": query, "limit": limit,
            },
        ).fetchall()

        return [{
            "tab_id": str(row.id),
            "title": row.title,
            "url": row.url,
            "summary": row.summary,
            "topic": row.topic,
            "favicon": row.favicon,
            "score": float(row.score),
        } for row in rows]
    
    def domain_search(self, domain: str, limit: int = 20):
        rows = (
            self.db.query(Tab)
            .filter(Tab.is_searchable == True)
            .filter(Tab.url.ilike(f"%{domain}%"))
            .limit(limit)
            .all()
        )

        return [
            {
                "tab_id": str(tab.id),
                "title": tab.title,
                "url": tab.url,
                "summary": tab.summary,
                "topic": tab.topic_ref.title if tab.topic_ref else None,
                "favicon": tab.favicon,
                "score": 100.0,
            }
            for tab in rows
        ]
