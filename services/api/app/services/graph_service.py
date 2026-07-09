from app.repositories.graph_repository import GraphRepository
from app.schemas.graph import GraphNode, GraphEdge, GraphResponse

class GraphService:
    def __init__(self, repository: GraphRepository):
        self.repository = repository

    # Topics
    def get_topics(self):
        return self.repository.get_topics()
    
    def get_topic_graph(self, topic_id: str) -> GraphResponse | None:
        topic = self.repository.get_topic(topic_id)

        if topic is None:
            return None
        
        nodes: list[GraphNode] = []
        edges: list[GraphEdge] = []

        nodes.append(GraphNode(
            id=topic.id, label=topic.title,
            type="topic",
        ))
        
        tabs = self.repository.get_tabs_for_topic(topic_id)

        for tab in tabs:
            nodes.append(GraphNode(
                id=tab.id, label=tab.title, type="tab"
            ))

            edges.append(GraphEdge(
                source=topic.id, target=tab.id, type="contains",
            ))

            for entity in tab.entities:
                nodes.append(GraphNode(
                    id=entity.id, label=entity.name, type="entity",
                ))

                edges.append(GraphEdge(
                    source=tab.id, target=entity.id, type="mentions",
                ))
        
        # Remove duplicate nodes
        unique_nodes = {
            node.id: node for node in nodes
        }

        return GraphResponse(
            nodes=list(unique_nodes.values()),
            edges=edges,
        )
    
    def get_entity_graph(self, entity_id: str) -> GraphResponse | None:
        entity = self.repository.get_entity(entity_id)

        if entity is None:
            return None
        
        nodes: list[GraphNode] = []
        edges: list[GraphEdge] = []

        nodes.append(GraphNode(
            id=entity.id, label=entity.name, type="entity",
        ))

        tabs = self.repository.get_tabs_for_entity(entity_id)

        for tab in tabs:
            nodes.append(GraphNode(
                id=tab.id, label=tab.title, type="tab",
            ))

            edges.append(GraphEdge(
                source=entity.id, target=tab.id, type="appears_in",
            ))

            if tab.topic_ref:
                nodes.append(GraphNode(
                    id=tab.topic_ref.id, label=tab.topic_ref.title, type="topic",
                ))

                edges.append(GraphEdge(
                    source=tab.id, target=tab.topic_ref.id, type="belongs_to",
                ))
        
        unique_nodes = {
            node.id: node for node in nodes
        }

        return GraphResponse(
            nodes=list(unique_nodes.values()),
            edges=edges,
        )