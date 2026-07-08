from sqlalchemy import text
from sqlalchemy.orm import Session

class GraphTraversalRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def neighbors(
      self, entity_id: str, limit: int = 10  
    ):
        query = text("""
SELECT
    e.id, e.name, e.entity_type, r.weight
FROM entity_relationships r
JOIN entities e ON (CASE 
    WHEN r.entity_a_id=:id
    THEN r.entity_b_id
    ELSE r.entity_a_id
    END
)=e.id
                     
WHERE r.entity_a_id=:id
OR r.entity_b_id=:id

ORDER BY r.weight DESC
                     
LIMIT :limit
""")
        rows = self.db.execute(query, {
            "id": entity_id, "limit": limit,
        })

        return [
            dict(row._mapping) for row in rows
        ]