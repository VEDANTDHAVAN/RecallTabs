from app.infrastructure.database.models.tab_entity import TabEntity

from app.repositories.tab_entity_repository import TabEntityRepository

from app.services.entity_graph_service import EntityGraphService
from app.services.entity_extraction_service import EntityExtractionService

class TabEntityService:
    def __init__(
        self, entity_service: EntityGraphService,
        extraction_service: EntityExtractionService,
        relation_repository: TabEntityRepository,
    ):
        self.entity_service = entity_service
        self.extraction_service = extraction_service
        self.relation_repository = relation_repository

    def process(self, tab_id: str, title: str, content: str):
        entities = self.extraction_service.extract(title, content)

        for item in entities:
            entity = self.entity_service.get_or_create(
                name=item["name"], entity_type=item["type"],
                summary=item.get("summary"),
            )

            existing = self.relation_repository.get(
                tab_id, entity.id,
            )

            if existing:
                self.relation_repository.increment_mentions(
                    tab_id, entity.id,
                )
                continue

            self.relation_repository.create(
                TabEntity(
                    tab_id=tab_id,
                    entity_id=entity.id,
                    mention_count=1,
                )
            )