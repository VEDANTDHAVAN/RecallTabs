from sqlalchemy.orm import Session

from app.infrastructure.database.models.entity_relationship import EntityRelationship

class EntityRelationshipRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, relationship: EntityRelationship) -> EntityRelationship:
        self.db.add(relationship)
        self.db.commit()
        self.db.refresh(relationship)

        return relationship
    
    def exists(
        self, source_entity_id: str, target_entity_id: str, relationship_type: str,
    ) -> EntityRelationship | None:
        return (
            self.db.query(EntityRelationship).filter(
                EntityRelationship.source_entity_id == source_entity_id,
                EntityRelationship.target_entity_id == target_entity_id,
                EntityRelationship.relationship_type == relationship_type,
            ).first()
        )
    
    def create_if_missing(
        self, source_entity_id: str, target_entity_id: str,
        relationship_type: str, confidence: float = 1.0,
    ) -> EntityRelationship:
        existing = self.exists(
            source_entity_id, target_entity_id, relationship_type,
        )

        if existing:
            return existing
        
        relationship = EntityRelationship(
            source_entity_id=source_entity_id, target_entity_id=target_entity_id,
            relationship_type=relationship_type, confidence=confidence,
        )

        return self.create(relationship)
    
    def outgoing(self, entity_id: str):
        return (
            self.db.query(EntityRelationship).filter(
                EntityRelationship.source_entity_id == entity_id
            ).all()
        )
    
    def incoming(self, entity_id: str):
        return (
            self.db.query(EntityRelationship).filter(
                EntityRelationship.target_entity_id == entity_id
            ).all()
        )