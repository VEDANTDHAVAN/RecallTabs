from datetime import datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector

from sqlalchemy import String, Float, DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )

    name: Mapped[str] = mapped_column(
        String, unique=True, index=True
    )

    entity_type: Mapped[str] = mapped_column(
        String, index=True
    )

    summary: Mapped[str] = mapped_column(
        String, nullable=True
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536), nullable=True
    )

    importance: Mapped[float] = mapped_column(
        Float, default=1.0, nullable=False
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