from app.repositories.graph_repository import GraphRepository

from app.services.graph_analysis_service import GraphAnalysisService

class RecommendationService:
    def __init__(self, repository: GraphRepository):
        self.repository = repository
        self.analysis = GraphAnalysisService(repository)

    def recommend_topics(self, limit: int = 10):
        pagerank = self.analysis.pagerank()

        topics = self.repository.get_topics()

        ranked = sorted(
            topics, key=lambda topic: pagerank.get(topic.id, 0),
            reverse=True,
        )

        return ranked[:limit]
    
    def recommend_tabs_for_topic(self, topic_id: str, limit: int = 10):
        related_topics = self.repository.related_topics(topic_id)

        tabs = []

        for topic in related_topics:
            tabs.extend(
                self.repository.get_tabs_for_topic(topic.id)
            )

        seen = set()

        recommendations = []

        for tab in tabs:
            if tab.id in seen:
                continue

            seen.add(tab.id)
            recommendations.append(tab)

            if len(recommendations) >= limit:
                break

        return recommendations
    
    def recommend_tabs_for_entity(
        self, entity_id: str, limit: int = 10,
    ):
        tabs = self.repository.get_tabs_for_entity(entity_id)

        recommendations = []
        seen = set()

        for tab in tabs:
            if tab.id in seen:
                continue

            seen.add(tab.id)
            recommendations.append(tab)

            if len(recommendations) >= limit:
                break

        return recommendations
    
    def trending_topics(self, limit: int = 10):
        pagerank = self.analysis.pagerank()

        topics = self.repository.get_topics()

        return sorted(
            topics, key=lambda topic: pagerank.get(topic.id, 0),
            reverse=True,
        )[:limit]
    
    def knowledge_hubs(self, limit: int = 20):
        centrality = self.analysis.degree_centrality()

        return sorted(
            centrality.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:limit]
    
    def bridges(self, limit: int = 20):
        scores = self.analysis.betweenness()

        return sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:limit]