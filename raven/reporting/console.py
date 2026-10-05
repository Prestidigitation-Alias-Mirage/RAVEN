from __future__ import annotations

from collections import Counter

from rich.console import Console
from rich.table import Table

from raven.schemas.result import EvaluationResult


def print_run_summary(run_id: str, results: list[EvaluationResult]) -> None:
    console = Console()
    counts = Counter(result.result.value for result in results)

    table = Table(title=f"RAVEN run {run_id}")
    table.add_column("Result")
    table.add_column("Count", justify="right")
    for state in ["PASS", "FAIL", "PARTIAL", "INDETERMINATE", "ERROR"]:
        table.add_row(state, str(counts.get(state, 0)))

    console.print(table)
