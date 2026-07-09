from sqlalchemy.orm import Session

from app.infrastructure.database.models.entity import Entity
from app.infrastructure.database.models.topic import Topic
from app.infrastructure.database.models.tab import Tab

class GraphRepository:
    def __init__(self, db: Session):
        self.db = db

    # Topics
    def get_topics(self) -> list[Topic]:
        return (
            self.db.query(Topic).order_by(Topic.importance.desc()).all()
        )
    
    def get_topic(self, topic_id: str) -> Topic | None:
        return (
            self.db.query(Topic).filter(Topic.id == topic_id).first()
        )
    
    # Entities
    def get_entity(self, entity_id: str) -> Entity | None:
        return (
            self.db.query(Entity).filter(Entity.id == entity_id).first()
        )
    
    def get_entities(self) -> list[Entity]:
        return (
            self.db.query(Entity).order_by(Entity.importance.desc()).all()
        )
    
    # Tabs
    def get_tabs_for_topic(self, topic_id: str) -> list[Tab]:
        return (
            self.db.query(Tab).filter(Tab.topic_id == topic_id).all()
        )
    
    def get_tabs_for_entity(self, entity_id: str) -> list[Tab]:
        entity = self.get_entity(entity_id)

        if entity is None:
            return []
        
        return list(entity.tabs)
    
    # Relationships
    def related_entities(
        self, entity_id: str
    ) -> list[Entity]:
        # entity = self.get_entity(entity_id)

        # if entity is None:
            #return []
        
        # return list(entity.related_entities)
        return []

    def related_topics(self, topic_id: str) -> list[Topic]:
        topic = self.get_topic(topic_id)

        if topic is None:
            return []
        
        related: set[Topic] = set()

        for tab in topic.tabs:
            for entity in tab.entities:
                for other_tab in entity.tabs:
                    if (
                        other_tab.topic_ref and other_tab.topic_ref.id != topic.id
                    ):
                        related.add(other_tab.topic_ref)

        return list(related)
    
    def get_tab(self, tab_id: str):
        return (
            self.db.query(Tab).filter(Tab.id == tab_id).first()
        )
    
    def get_topic_tabs(self, topic_id: str):
        return self.get_tabs_for_topic(topic_id)