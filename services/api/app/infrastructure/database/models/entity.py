from datetime import datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector

from sqlalchemy import String, Float, DateTime, Integer, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )
    # Canonical entity name
    name: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536), nullable=True
    )

    confidence: Mapped[float] = mapped_column(
        Float, default=1.0, nullable=False
    )

    importance: Mapped[float] = mapped_column(
        Float, default=1.0, nullable=False
    )

    mention_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False,
    )

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    aliases = relationship(
        "EntityAlias", back_populates="entity",
        cascade="all, delete-orphan",
    )

    tabs = relationship(
        "TabEntity", back_populates="entity",
        cascade="all, delete-orphan",
    )

    relationships = relationship(
        "EntityRelationship", foreign_keys="EntityRelationship.source_entity_id",
        back_populates="source_entity", cascade="all, delete-orphan",
    )