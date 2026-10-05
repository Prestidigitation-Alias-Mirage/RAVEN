from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    name: str = "local-baseline"
    suite: str = "baseline"
    max_iterations: int = Field(default=1, ge=1, le=100)
    seed: int = 1337


class AuthorizationConfig(BaseModel):
    confirmed: bool = False
    scope_reference: str = ""


class TargetConfig(BaseModel):
    adapter: str = "mock"
    name: str = "local-test-target"
    model: str = "mock-v0"


class EvaluationConfig(BaseModel):
    strategy: str = "rules"


class StorageConfig(BaseModel):
    backend: str = "jsonl"
    directory: str = "runs"


class SafetyConfig(BaseModel):
    request_budget: int = Field(default=100, ge=1, le=10_000)
    max_concurrency: int = Field(default=1, ge=1, le=32)
    max_mutation_depth: int = Field(default=0, ge=0, le=32)
    request_timeout_seconds: int = Field(default=30, ge=1, le=600)
    allowed_targets: list[str] = Field(default_factory=lambda: ["mock"])


class RavenConfig(BaseModel):
    run: RunConfig = Field(default_factory=RunConfig)
    authorization: AuthorizationConfig = Field(default_factory=AuthorizationConfig)
    target: TargetConfig = Field(default_factory=TargetConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)


def load_config(path: str | Path) -> RavenConfig:
    config_path = Path(path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    config = RavenConfig.model_validate(raw)

    if not config.authorization.confirmed:
        raise ValueError("authorization.confirmed must be true before a RAVEN run")
    if not config.authorization.scope_reference.strip():
        raise ValueError("authorization.scope_reference must identify the approved test scope")
    if config.target.adapter not in config.safety.allowed_targets:
        raise ValueError(
            f"target adapter '{config.target.adapter}' is not present in safety.allowed_targets"
        )
    if config.storage.backend != "jsonl":
        raise ValueError("v0.1 currently supports only the jsonl storage backend")
    if config.evaluation.strategy != "rules":
        raise ValueError("v0.1 currently supports only the deterministic rules evaluator")

    return config
