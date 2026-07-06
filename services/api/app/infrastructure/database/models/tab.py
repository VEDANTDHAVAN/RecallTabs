from uuid import uuid4
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, Integer, DateTime, JSON, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    topic_id: Mapped[str | None] = mapped_column(
        ForeignKey("topics.id"), nullable=True
    )

    topic_ref = relationship(
        "Topic", back_populates="tabs",
    )

    category: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    is_searchable: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False,
    )

    importance_score: Mapped[float] = mapped_column(
        Float, default=50.0, nullable=False,
    )

    open_count: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False,
    )

    total_time_spent: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False,
    )

    last_opened_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True,
    )

    last_chat_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True,
    )

    chat_reference_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False,
    )