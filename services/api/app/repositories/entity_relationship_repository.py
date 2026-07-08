from sqlalchemy.orm import Session

from app.infrastructure.database.models.entity_relationship import EntityRelationship

class EntityRelationshipRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, relationship):
        self.db.add(relationship)
        self.db.commit()
        self.db.refresh(relationship)

        return relationship
    
    def update(self, relationship):
        self.db.add(relationship)
        self.db.commit()
        self.db.refresh(relationship)

        return relationship
    
    def get(self, entity_a, entity_b):
        return (
            self.db.query(EntityRelationship).filter(
                EntityRelationship.entity_a_id == entity_a,
                EntityRelationship.entity_b_id == entity_b,
            ).first()
        )