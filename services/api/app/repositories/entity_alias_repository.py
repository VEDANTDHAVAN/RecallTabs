from sqlalchemy.orm import Session

from app.infrastructure.database.models.entity_alias import EntityAlias

class EntityAliasRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, alias: EntityAlias) -> EntityAlias:
        self.db.add(alias)
        self.db.commit()
        self.db.refresh(alias)

        return alias

    def get(self, alias: str) -> EntityAlias | None:
        return (
            self.db.query(EntityAlias).filter(EntityAlias.alias == alias).first()
        )