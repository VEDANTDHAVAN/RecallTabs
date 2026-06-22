from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.database.models.tab_chunk import TabChunk

class TabChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tab_chunk: TabChunk):
        self.db.add(tab_chunk)
        self.db.commit()
        self.db.refresh(tab_chunk)

        return tab_chunk
    
    def semantic_search(self, embedding: list[float], limit: int = 5,):
        vector_str = "["+",".join(
            map(str, embedding)
        ) + "]"
        
        sql = text("""
SELECT

    t.id as tab_id,

    t.title,

    t.url,

    MAX(
        1 - (
            tc.embedding <=> CAST(:embedding AS vector)
        )
    ) AS score

FROM tab_chunk tc

JOIN tabs t

    ON tc.tab_id = t.id

GROUP BY

    t.id,
    t.title,
    t.url

ORDER BY score DESC

LIMIT :limit     
""")

        rows = self.db.execute(
            sql, {
                "embedding": vector_str, "limit": limit,
            }
        ).fetchall()

        return [
            {
                "tab_id": row.tab_id,
                "title": row.title,
                "url": row.url,
                "score": float(row.score),
            }

            for row in rows
        ]
    
    def search_chunks(
        self, embedding: list[float], limit: int = 5,
    ):
        query = text("""
SELECT
    tc.chunk_text, t.title, t.url,
    1-(tc.embedding <=> CAST(:embedding AS vector))
    AS score
FROM tab_chunk tc
JOIN tabs t
    ON tc.tab_id = t.id
ORDER BY
    tc.embedding <=> CAST(:embedding AS vector)
LIMIT :limit
""")
        result = self.db.execute(
            query, {
                "embedding": str(embedding),
                "limit": limit,
            }
        )

        return [
            dict(row._mapping) for row in result
        ]
    
    def get_chunks_by_tab_id(self, tab_id: str,) -> list[TabChunk]:
        return (
            self.db.query(TabChunk)
            .filter(TabChunk.tab_id == tab_id).all()
        )