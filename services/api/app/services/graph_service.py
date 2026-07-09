from app.repositories.graph_repository import GraphRepository

class GraphService:
    def __init__(self, repository: GraphRepository):
        self.repository = repository

    # Topics
    def get_topics(self):
        return self.repository.get_topics()
    
    def get_topic_graph(self, topic_id: str):
        topic = self.repository.get_topic(topic_id)

        if topic is None:
            return None
        
        tabs = self.repository.get_tabs_for_topic(topic_id)

        related_topics = self.repository.related_topics(topic_id)

        return {
            "topic": topic,
            "tabs": tabs,
            "related_topics": related_topics,
        }
    
    # Entities
    def get_entity_graph(self, entity_id: str):
        entity = self.repository.get_entity(entity_id)

        if entity is None:
            return None
        
        tabs = self.repository.get_tabs_for_entity(entity_id)

        return {
            "entity": entity,
            "tabs": tabs,
        }