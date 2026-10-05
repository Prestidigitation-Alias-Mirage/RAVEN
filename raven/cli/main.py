from __future__ import annotations

import asyncio
import json
from collections import Counter
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from raven.core.config import load_config
from raven.core.orchestrator import Orchestrator
from raven.reporting.console import print_run_summary
from raven.targets.mock import MockTarget

app = typer.Typer(help="RAVEN authorized LLM security evaluation CLI")
console = Console()

DEFAULT_CONFIG_PATH = Path("configs/example.yaml")
DEFAULT_RUNS_DIR = Path("runs")


def _suite_path(name: str) -> Path:
    return Path("suites") / name / "suite.yaml"


@app.command("validate-config")
def validate_config(
    config: Annotated[Path, typer.Argument()] = DEFAULT_CONFIG_PATH,
) -> None:
    """Validate configuration and authorization/safety gates."""
    loaded = load_config(config)
    console.print(
        f"[green]valid[/green]: target={loaded.target.adapter} "
        f"scope={loaded.authorization.scope_reference}"
    )


@app.command()
def run(
    target: Annotated[str, typer.Option("--target")] = "mock",
    suite: Annotated[str, typer.Option("--suite")] = "baseline",
    config: Annotated[Path, typer.Option("--config")] = DEFAULT_CONFIG_PATH,
) -> None:
    """Run a fixed suite against an explicitly authorized target adapter."""
    loaded = load_config(config)

    if target != loaded.target.adapter:
        raise typer.BadParameter(
            f"--target {target!r} does not match configured adapter "
            f"{loaded.target.adapter!r}"
        )

    if suite != loaded.run.suite:
        raise typer.BadParameter(
            f"--suite {suite!r} does not match configured suite "
            f"{loaded.run.suite!r}"
        )

    if target != "mock":
        raise typer.BadParameter("v0.1 enables only the local mock target")

    orchestrator = Orchestrator(
        loaded,
        MockTarget(loaded.target.name),
    )

    run_id, results = asyncio.run(
        orchestrator.run(
            config,
            _suite_path(suite),
        )
    )

    print_run_summary(run_id, results)
    console.print(
        f"[green]archived[/green]: "
        f"{loaded.storage.directory}/{run_id}"
    )


@app.command()
def report(
    run_id: str,
    runs_dir: Annotated[Path, typer.Option("--runs-dir")] = DEFAULT_RUNS_DIR,
) -> None:
    """Summarize an archived run without re-executing it."""
    evaluations_path = runs_dir / run_id / "evaluations.jsonl"

    if not evaluations_path.exists():
        raise typer.BadParameter(f"run not found: {run_id}")

    counts: Counter[str] = Counter()

    for line in evaluations_path.read_text(
        encoding="utf-8"
    ).splitlines():
        if line.strip():
            counts[json.loads(line)["result"]] += 1

    console.print(f"RAVEN report: {run_id}")

    for state in [
        "PASS",
        "FAIL",
        "PARTIAL",
        "INDETERMINATE",
        "ERROR",
    ]:
        console.print(
            f"  {state:13} {counts.get(state, 0)}"
        )


if __name__ == "__main__":
    app()
