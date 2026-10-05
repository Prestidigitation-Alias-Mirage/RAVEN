from __future__ import annotations

from pathlib import Path

import yaml

from raven.schemas.testcase import TestCase


def load_suite(path: str | Path) -> list[TestCase]:
    suite_path = Path(path)
    raw = yaml.safe_load(suite_path.read_text(encoding="utf-8")) or {}
    cases = raw.get("cases", [])
    if not cases:
        raise ValueError(f"suite contains no cases: {suite_path}")

    return [TestCase.model_validate(case) for case in cases]
