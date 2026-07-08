from uuid import uuid4
from datetime import datetime

from sqlalchemy import String, Float, DateTime, ForeignKey, UniqueConstraint

from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.database.base import Base

class EntityRelationship(Base):
    __tablename__="entity_relationships"

    __table_args__=(
        UniqueConstraint(
            "entity_a_id", "entity_b_id",
        ),
    )

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4()),
    )

    entity_a_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id"),
    )

    entity_b_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id"),
    )

    weight: Mapped[float] = mapped_column(
        Float, default=1.0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow,
    )