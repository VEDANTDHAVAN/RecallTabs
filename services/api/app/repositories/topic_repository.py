from sqlalchemy import func

from app.infrastructure.database.models.tab import Tab

class TopicRepository:
    def __init__(self, db):
        self.db = db

    def get_topics(self):
        return (
            self.db.query(
                Tab.topic, func.count(Tab.id).label("count")
            ).filter(
                Tab.topic.isnot(None)
            ).group_by(Tab.topic).order_by(
                func.count(Tab.id).desc()
            ).all()
        )
    
    def get_tabs_by_topic(
        self, topic: str,
    ):
        return (
            self.db.query(Tab).filter(
                Tab.topic == topic
            ).order_by(Tab.captured_at.desc()).all()
        )