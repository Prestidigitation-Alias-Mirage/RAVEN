from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from raven.core.config import RavenConfig
from raven.core.run_context import (
    create_run_id,
    current_git_commit,
    current_git_dirty,
    sha256_file,
)
from raven.core.suite_loader import load_suite
from raven.evaluation.rules import RuleEvaluator
from raven.schemas.result import EvaluationResult
from raven.schemas.run import RunManifest
from raven.storage.jsonl import JsonlArchivist
from raven.targets.base import TargetAdapter


class Orchestrator:
    def __init__(self, config: RavenConfig, target: TargetAdapter) -> None:
        self.config = config
        self.target = target
        self.evaluator = RuleEvaluator()

    async def run(
        self, config_path: str | Path, suite_path: str | Path
    ) -> tuple[str, list[EvaluationResult]]:
        testcases = load_suite(suite_path)
        if len(testcases) > self.config.safety.request_budget:
            raise ValueError(
                f"suite contains {len(testcases)} cases but request_budget is "
                f"{self.config.safety.request_budget}"
            )

        run_id = create_run_id()
        archive = JsonlArchivist(self.config.storage.directory, run_id)
        manifest = RunManifest(
            run_id=run_id,
            suite=self.config.run.suite,
            target=self.config.target.name,
            model=self.config.target.model,
            seed=self.config.run.seed,
            raven_commit=current_git_commit(),
            working_tree_dirty=current_git_dirty(),
            config_hash=sha256_file(config_path),
            started_at=datetime.now(UTC),
        )
        archive.write_json("manifest.json", manifest)
        archive.write_json("config.json", self.config.model_dump(mode="json"))

        evaluations: list[EvaluationResult] = []
        for testcase in testcases:
            response = await self.target.execute(testcase)
            evaluation = self.evaluator.evaluate(testcase, response, run_id)
            archive.append_jsonl("cases.jsonl", testcase)
            archive.append_jsonl("responses.jsonl", response)
            archive.append_jsonl("evaluations.jsonl", evaluation)
            evaluations.append(evaluation)

        return run_id, evaluations
