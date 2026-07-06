from datetime import datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector

from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class Topic(Base):
    __tablename__="topics"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4()),
    )

    title: Mapped[str] = mapped_column(
        String, unique=True, index=True,
    )

    summary: Mapped[str | None] = mapped_column(
        String, nullable=True,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536), nullable=True,
    )

    importance: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    tabs = relationship(
        "Tab", back_populates="topic_ref",
    )