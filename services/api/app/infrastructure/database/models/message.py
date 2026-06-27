from uuid import uuid4

from sqlalchemy import Text, String, ForeignKey

from sqlalchemy.dialects.postgresql import JSON

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )

    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id"), index=True, nullable=False
    )

    role: Mapped[str] = mapped_column(String, nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    conversation = relationship(
        "Conversation", back_populates="messages"
    )

    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)