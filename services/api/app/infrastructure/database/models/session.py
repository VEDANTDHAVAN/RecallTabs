from uuid import uuid4

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
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