import networkx as nx

from app.repositories.graph_repository import GraphRepository

from networkx.algorithms.community import greedy_modularity_communities

class GraphAnalysisService:
    def __init__(self, repository: GraphRepository):
        self.repository = repository

    def build_graph(self) -> nx.Graph:
        G = nx.Graph()

        # Topics
        topics = self.repository.get_topics()

        for topic in topics:
            G.add_node(topic.id, label=topic.title, type="topic")

            tabs = self.repository.get_tabs_for_topic(topic.id)

            for tab in tabs:
                G.add_node(
                    tab.id, label=tab.title, type="tab",
                )

                G.add_edge(
                    topic.id, tab.id, relationship="contains",
                )

                for entity in tab.entities:
                    G.add_node(
                        entity.id, label=entity.name, type="entity",
                    )

                    G.add_edge(
                        tab.id, entity.id, relationship="mentions",
                    )
            
        return G
    
    def pagerank(self):
        G = self.build_graph()

        return nx.pagerank(G)
    
    def degree_centrality(self):
        G = self.build_graph()

        return nx.degree_centrality(G)
    
    def betweenness(self):
        G = self.build_graph()

        return nx.betweenness_centrality(G)
    
    def connected_components(self):
        G = self.build_graph()

        return [
            list(component) for component in nx.connected_components(G)
        ]
    
    def shortest_path(
        self, source: str, target: str,
    ):
        G = self.build_graph()

        if not (
            G.has_node(source) and G.has_node(target)
        ):
            return []
        
        try:
            return nx.shortest_path(
                G, source, target,
            )
        
        except nx.NetworkXNoPath:
            return []
        
    def communities(self):
        G = self.build_graph()

        groups = greedy_modularity_communities(G)

        return [
            list(group) for group in groups
        ]
    
    def statistics(self):
        G = self.build_graph()

        return {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": nx.density(G),
            "components": nx.number_connected_components(G),
        }