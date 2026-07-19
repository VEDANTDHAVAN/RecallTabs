from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class ProviderConfig:
    provider: str
    model: str

    api_key: str | None = None
    base_url: str | None = None

    timeout: float = 120.0
    
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float | None = None
    seed: int | None = None

    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.provider = self.provider.lower().strip()

        if self.base_url:
            self.base_url = self.base_url.rstrip("/")

        if not self.provider:
            raise ValueError("provider cannot be empty")
        
        if not self.model:
            raise ValueError("model cannot be empty")
        
    def generate_kwargs(self) -> dict[str, Any]:
        # common generation parameters supported by most providers
        kwargs: dict[str, Any] = {
            "temperature": self.temperature,
        }

        if self.max_tokens is not None:
            kwargs["max_tokens"] = self.max_tokens

        if self.top_p is not None:
            kwargs["top_p"] = self.top_p

        if self.seed is not None:
            kwargs["seed"] = self.seed

        kwargs.update(self.extra)

        return kwargs