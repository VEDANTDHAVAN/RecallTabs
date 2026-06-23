from collections import defaultdict

class TimelineService:
    def __init__(self, repository):
        self.repository = repository

    def get_timeline(self):
        tabs = self.repository.get_timeline()

        grouped = defaultdict(list)

        for tab in tabs:
            date = (
                tab.captured_at.strftime("%Y-%m-%d")
            )

            grouped[date].append({
                "id": tab.id, "title": tab.title, "url": tab.url,
                "topic": tab.topic or "Unknown", "summary": tab.summary or "No AI summary available",
            })

        return [
            {
                "date": date, "tabs": grouped[date],
            } for date in sorted(
                grouped.keys(), reverse=True,
            )
        ]
    
    def topic_stats(self):
        return (
            self.repository.topic_statistics()
        )