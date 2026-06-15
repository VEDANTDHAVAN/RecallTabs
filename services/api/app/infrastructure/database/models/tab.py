from uuid import uuid4

from sqlalchemy import String, Text, ForeignKey
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

    url: Mapped[str] = mapped_column(Text,)

    title: Mapped[str] = mapped_column(Text,)

    content: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )