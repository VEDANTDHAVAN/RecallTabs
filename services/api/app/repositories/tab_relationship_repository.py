from app.infrastructure.database.models.tab_relationships import TabRelationship
from sqlalchemy import text

class TabRelationshipRepository:
    def __init__(self, db):
        self.db = db

    def create(
        self, source_id, related_id, score,
    ):
        relation = TabRelationship(
            source_tab_id=source_id,
            related_tab_id=related_id,
            similarity_score=score,
        )

        self.db.add(relation)
        self.db.commit()

        return relation
    
    def get_related(self, tab_id: str, limit: int = 10):
        query = text("""
            SELECT
                t.id, t.title, t.url,
                tr.similarity_score
            FROM tab_relationships tr
            JOIN tabs t
                ON t.id = tr.related_tab_id
            WHERE
                tr.source_tab_id = :tab_id
            ORDER BY
                tr.similarity_score DESC
            LIMIT :limit
            """)

        rows = self.db.execute(
            query,
            {
                "tab_id": tab_id,
                "limit": limit,
            }
        )

        return [
            dict(r._mapping)
            for r in rows
        ]