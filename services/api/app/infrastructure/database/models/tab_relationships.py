from uuid import uuid4

from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.database.base import Base

class TabRelationship(Base):
    __tablename__ = "tab_relationships"

    id: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid4())
    )

    source_tab_id: Mapped[str] = mapped_column(
        ForeignKey("tabs.id")
    )

    related_tab_id: Mapped[str] = mapped_column(
        ForeignKey("tabs.id")
    )

    similarity_score: Mapped[float] = mapped_column(Float)