from app.domain.tab.schemas import CreateTabRequest
from app.infrastructure.database.models.tab import Tab
from app.repositories.tab_repository import TabRepository

class TabService:
    def __init__(self, repository: TabRepository):
        self.repository = repository
    
    def create_tab(self, user_id: str, 
        payload: CreateTabRequest,
    ):
        return self.repository.create(
            Tab(
                user_id=user_id,
                url=str(payload.url),
                title=payload.title,
                content=payload.content,
            )
        )
    
    def list_tabs(
        self, user_id: str,
    ): 
        return self.repository.list_by_user(user_id=user_id)
