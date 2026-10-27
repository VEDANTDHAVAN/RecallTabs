from dataclasses import dataclass, field

from app.infrastructure.database.models.entity import Entity

@dataclass(slots=True)
class ExtractionResult:
    language: str
    entities: list[Entity] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    embedding: list[float] | None = None
    summary: str | None = None
    importance: float = 1.0