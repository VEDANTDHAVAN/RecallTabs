from sqlalchemy.orm import Session

from app.infrastructure.database.models.tab_entity import TabEntity

class TabEntityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, relation: TabEntity) -> TabEntity:
        self.db.add(relation)
        self.db.commit()
        self.db.refresh(relation)

        return relation

    def get(self, tab_id: str, entity_id: str) -> TabEntity | None:
        return (
            self.db.query(TabEntity).filter(
                TabEntity.tab_id == tab_id,
                TabEntity.entity_id == entity_id,
            ).first()
        )

    def get_entities(self, tab_id: str) -> list[TabEntity]:
        return (
            self.db.query(TabEntity).filter(TabEntity.tab_id == tab_id).all()
        )

    def update(self, relation: TabEntity) -> TabEntity:
        self.db.add(relation)
        self.db.commit()
        self.db.refresh(relation)

        return relation

    def increment_mentions(
        self, tab_id: str, entity_id: str,
    ) -> TabEntity:
        relation = self.get(tab_id, entity_id)

        if relation:
            relation.mention_count += 1
            return self.update(relation)

        raise ValueError("TabEntity relation not found")