from uuid import uuid4
from datetime import datetime

from sqlalchemy import String, Float, DateTime, ForeignKey, UniqueConstraint

from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.database.base import Base

class EntityRelationship(Base):
    __tablename__="entity_relationships"

    __table_args__=(
        UniqueConstraint(
            "source_entity_id", "target_entity_id", 
            "relationship_type", name="uq_entity_relationship",
        ),
    )

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4()),
    )

    source_entity_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id"), index=True,
    )

    target_entity_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id"), index=True,
    )

    relationship_type: Mapped[str] = mapped_column(
        String(64),
    )

    confidence: Mapped[float] = mapped_column(
        Float, default=1.0, nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow,
    )