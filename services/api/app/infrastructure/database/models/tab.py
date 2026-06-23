from uuid import uuid4
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class Tab(Base):
    __tablename__ = "tabs"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, 
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), index=True,
    )

    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("sessions.id"), nullable=True
    )

    url: Mapped[str] = mapped_column(Text,)

    title: Mapped[str] = mapped_column(Text,)

    content: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True,
    )

    favicon: Mapped[str | None] = mapped_column(
        Text, nullable=True,
    )

    word_count: Mapped[int] = mapped_column(
        Integer, default=0,
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow,
    )

    summary: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    keywords: Mapped[list | None] = mapped_column(
        JSON, nullable=True
    )

    topic: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    category: Mapped[str | None] = mapped_column(
        String, nullable=True
    )