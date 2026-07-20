from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class EmbeddingProviderConfig:
    provider: str
    model: str
    api_key: str | None = None
    base_url: str | None = None
    timeout: float = 60.0
    dimensions: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)