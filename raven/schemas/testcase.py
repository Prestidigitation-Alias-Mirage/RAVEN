from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TestCase(BaseModel):
    """Immutable description of one security evaluation case."""

    model_config = ConfigDict(frozen=True)

    id: str
    category: str
    prompt: str
    objective: str
    parent_id: str | None = None
    mutation_strategy: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
