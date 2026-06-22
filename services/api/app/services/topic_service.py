class TopicService:
    def __init__(self, repository):
        self.repository = repository

    def get_topics(self):
        rows = self.repository.get_topics()

        return [
            {
                "topic": r.topic,
                "count": r.count,
            }
            for r in rows
        ]

    def get_topic_tabs(self, topic: str,):
        tabs = (
            self.repository.get_tabs_by_topic(topic)
        )

        return [
            {
                "id": tab.id,
                "title": tab.title,
                "url": tab.url,
                "summary": tab.summary,
                "category": tab.category,
                "keywords": tab.keywords,
            }
            for tab in tabs
        ]