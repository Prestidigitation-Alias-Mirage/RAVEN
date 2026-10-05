from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RunManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    suite: str
    target: str
    model: str
    seed: int
    raven_commit: str
    working_tree_dirty: bool
    config_hash: str
    started_at: datetime
