from uuid import uuid4

from sqlalchemy import String, Float, Integer, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class TabEntity(Base):
    __tablename__ = "tab_entities"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )

    tab_id: Mapped[str] = mapped_column(
        ForeignKey("tabs.id", ondelete="CASCADE"), index=True
    )

    entity_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"), index=True
    )

    confidence: Mapped[float] = mapped_column(
        Float, default=1.0, nullable=False
    )

    mention_count: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False,
    )

    tab = relationship(
        "Tab", back_populates="entities"
    )

    entity = relationship(
        "Entity", back_populates="tabs"
    )