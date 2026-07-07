from sqlalchemy import text
from sqlalchemy.orm import Session

class KnowledgeGraphRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_entity_graph(self, entity_name: str):
        query = text("""
SELECT
                     
    e.id AS entity_id, e.name, e.entity_type,
    t.id AS tab_id, t.title, t.url,
    tp.title AS topic, s.title AS session,
    mc.title AS cluster
FROM entities e
JOIN tab_entity te ON te.entity_id = e.id
JOIN tabs t ON te.tab_id = t.id
LEFT JOIN topics tp ON tp.id = t.topic_id
LEFT JOIN sessions s ON s.id = t.session_id
LEFT JOIN memory_clusters mc ON mc.id = s.cluster_id
WHERE lower(e.name)=lower(:name)
                    
ORDER BY
    mc.importance DESC NULLS LAST,
    tp.importance DESC NULLS LAST,
    t.importance DESC NULLS LAST
""")
        rows = self.db.execute(query, {
            "name": entity_name,
        })

        return [
            dict(row._mapping) for row in rows
        ]