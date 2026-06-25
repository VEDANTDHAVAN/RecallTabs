from uuid import uuid4

from sqlalchemy import String, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )

    title: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    messages = relationship(
        "Message", cascade="all, delete-orphan",
        back_populates="conversation"
    )