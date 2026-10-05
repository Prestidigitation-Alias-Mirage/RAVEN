from pathlib import Path

import pytest

from raven.core.config import load_config
from raven.core.orchestrator import Orchestrator
from raven.schemas.result import EvaluationState
from raven.targets.mock import MockTarget


@pytest.mark.asyncio
async def test_end_to_end_baseline(tmp_path: Path) -> None:
    config = load_config("configs/example.yaml")
    config.storage.directory = str(tmp_path / "runs")
    orchestrator = Orchestrator(config, MockTarget(config.target.name))

    run_id, results = await orchestrator.run(
        "configs/example.yaml",
        "suites/baseline/suite.yaml",
    )

    assert len(results) == 3
    assert all(result.result == EvaluationState.PASS for result in results)
    run_dir = tmp_path / "runs" / run_id
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "cases.jsonl").exists()
    assert (run_dir / "responses.jsonl").exists()
    assert (run_dir / "evaluations.jsonl").exists()
