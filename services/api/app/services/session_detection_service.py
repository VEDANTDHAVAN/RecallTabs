from app.infrastructure.database.models.session import Session
from app.repositories.session_repository import SessionRepository
from app.repositories.tab_repository import TabRepository

class SessionDetectionService:
    def __init__(
        self, session_repository: SessionRepository,
        tab_repository: TabRepository,
    ):
        self.session_repository = session_repository
        self.tab_repository = tab_repository

    async def assign_session(self, tab):
        topic = tab.topic
        if not topic:
            return None

        existing = (
            self.session_repository.get_by_topic(topic, user_id=tab.user_id)
        )

        if existing:
            tab.session_id = existing.id
            self.tab_repository.update(tab)

            return existing

        session = Session(
            user_id=tab.user_id, title=topic, topic=topic,
            summary=tab.summary,
        )

        saved = self.session_repository.create(session)

        tab.session_id = saved.id

        self.tab_repository.update(tab)

        return saved
