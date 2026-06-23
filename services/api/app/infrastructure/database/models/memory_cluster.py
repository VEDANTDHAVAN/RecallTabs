from uuid import uuid4

from pgvector.sqlalchemy import Vector

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class MemoryCluster(Base):
    __tablename__ = "memory_clusters"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )

    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    summary: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384), nullable=False,
    )