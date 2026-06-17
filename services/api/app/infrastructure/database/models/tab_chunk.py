from uuid import uuid4

from sqlalchemy import ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column

from pgvector.sqlalchemy import Vector

from app.infrastructure.database.base import Base

class TabChunk(Base):
    __tablename__ = "tab_chunk"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4())
    )

    tab_id: Mapped[str] = mapped_column(
        ForeignKey("tabs.id"), index=True
    )

    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(Vector(384), nullable=False)
# Why Vector(384)?

# We'll use: sentence-transformers/all-MiniLM-L6-v2
# because: Small, Fast, Excellent, quality, Embedding size = 384
