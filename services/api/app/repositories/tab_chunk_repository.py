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
    
    def semantic_search(self, embedding: list[float], limit: int = 10,):
        vector_str = "["+",".join(map(str, embedding)) + "]"
        
        sql = text("""
SELECT DISTINCT on (t.id)

    t.id as tab_id,
    t.title, t.url,
    t.summary, t.topic,
    t.favicon, t.captured_at, 
    1 - (
        tc.embedding <=> CAST(:embedding AS vector)
    ) AS score
FROM tab_chunk tc
JOIN tabs t
    ON tc.tab_id = t.id
WHERE t.summary IS NOT NULL
      AND LENGTH(t.summary) > 30 
AND t.url NOT LIKE 'http://localhost%'
AND t.url NOT LIKE 'https://localhost%'
AND t.url NOT LIKE 'http://127.%'
AND t.url NOT LIKE 'chrome://%'
AND t.url NOT LIKE 'chrome-extension://%'
AND t.url NOT LIKE 'edge://%'
AND t.url NOT LIKE '%supabase.com/dashboard%'
ORDER BY
    t.id, tc.embedding <=> CAST(:embedding AS vector),
    t.captured_at DESC
LIMIT :limit     
""")

        rows = self.db.execute(
            sql, {
                "embedding": vector_str, "limit": limit,
            }
        ).fetchall()

        results = []

        for row in rows:
            score = round(float(row.score) * 100, 1)
            if score < 45:
                continue

            results.append({
                "tab_id": str(row.tab_id),
                "title": row.title,
                "url": row.url,
                "summary": row.summary,
                "topic": row.topic,
                "favicon": row.favicon,
                "captured_at": row.captured_at,
                "score": score,
            })

        return results
    
    def search_chunks(
        self, embedding: list[float], limit: int = 5,
    ):
        vector_str = "[" + ",".join(map(str, embedding)) + "]"

        query = text("""
SELECT
    tc.chunk_text, t.id AS tab_id, t.title, t.url,
    t.summary, t.topic, t.favicon,
    1-(tc.embedding <=> CAST(:embedding AS vector))
    AS score
FROM tab_chunk tc
JOIN tabs t
    ON tc.tab_id = t.id
WHERE 
    LENGTH(tc.chunk_text) > 80
ORDER BY
    tc.embedding <=> CAST(:embedding AS vector)
LIMIT :limit
""")
        rows = self.db.execute(
            query, {
                "embedding": vector_str,
                "limit": limit,
            },
        ).fetchall()

        return [
            {
                "tab_id": row.tab_id,
                "title": row.title,
                "url": row.url,
                "summary": row.summary,
                "topic": row.topic,
                "favicon": row.favicon,
                "chunk_text": row.chunk_text,
                "score": round(float(row.score) * 100, 1),
            }
            for row in rows
        ]
    
    def get_chunks_by_tab_id(self, tab_id: str,) -> list[TabChunk]:
        return (
            self.db.query(TabChunk)
            .filter(TabChunk.tab_id == tab_id).all()
        )
