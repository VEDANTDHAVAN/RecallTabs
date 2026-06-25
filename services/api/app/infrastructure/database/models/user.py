from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class User(Base):
    __tablename__ = "users"


    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4()),
    )

    clerk_user_id: Mapped[str] = mapped_column(
        String, unique=True, index=True,
    )

    email: Mapped[str] = mapped_column(
        String, unique=True, index=True,
    )

    created_at: Mapped[str] = mapped_column(
        DateTime, default=datetime.utcnow,
    )

    conversations = relationship(
        "Conversation", backref="user", 
        cascade="all, delete-orphan"
    )