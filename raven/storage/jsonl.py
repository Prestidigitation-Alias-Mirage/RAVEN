from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class JsonlArchivist:
    def __init__(self, root: str | Path, run_id: str) -> None:
        self.run_dir = Path(root) / run_id
        self.run_dir.mkdir(parents=True, exist_ok=False)

    @staticmethod
    def _serializable(value: BaseModel | dict[str, Any]) -> dict[str, Any]:
        if isinstance(value, BaseModel):
            return value.model_dump(mode="json")
        return value

    def write_json(self, name: str, value: BaseModel | dict[str, Any]) -> None:
        path = self.run_dir / name
        path.write_text(
            json.dumps(self._serializable(value), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def append_jsonl(self, name: str, value: BaseModel | dict[str, Any]) -> None:
        path = self.run_dir / name
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(self._serializable(value), sort_keys=True) + "\n")
