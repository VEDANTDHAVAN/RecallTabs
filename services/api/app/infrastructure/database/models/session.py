from uuid import uuid4

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    topic: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    summary: Mapped[str] = mapped_column(
        Text, nullable=True
    )

    cluster_id: Mapped[str | None] = mapped_column(
        ForeignKey("memory_clusters.id"),
        nullable=True,
    )