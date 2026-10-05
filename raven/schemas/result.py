from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EvaluationState(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    INDETERMINATE = "INDETERMINATE"
    ERROR = "ERROR"


class TargetResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    testcase_id: str
    target_id: str
    content: str
    latency_ms: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    testcase_id: str
    target_id: str
    run_id: str
    result: EvaluationState
    evaluator: str
    reason: str
    evidence: list[str] = Field(default_factory=list)
    timestamp: datetime
