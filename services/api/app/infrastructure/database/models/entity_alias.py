from uuid import uuid4

from sqlalchemy import String, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class EntityAlias(Base):
    __tablename__="entity_aliases"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4()),
    )

    alias: Mapped[str] = mapped_column(
        String, unique=True, index=True
    )

    entity_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"), index=True,
    )

    entity = relationship(
        "Entity", back_populates="aliases"
    )