from __future__ import annotations

from datetime import UTC, datetime

from raven.schemas.result import EvaluationResult, EvaluationState, TargetResponse
from raven.schemas.testcase import TestCase


class RuleEvaluator:
    name = "deterministic-rules-v0.1"

    def evaluate(
        self,
        testcase: TestCase,
        response: TargetResponse,
        run_id: str,
    ) -> EvaluationResult:
        expected = testcase.metadata.get("expected", {})
        forbidden = [str(x) for x in expected.get("forbidden_substrings", [])]
        required = [str(x) for x in expected.get("required_substrings", [])]

        evidence: list[str] = []
        failures: list[str] = []

        for value in forbidden:
            if value in response.content:
                failures.append(f"forbidden substring observed: {value!r}")
        for value in required:
            if value not in response.content:
                failures.append(f"required substring missing: {value!r}")

        if failures:
            state = EvaluationState.FAIL
            reason = "; ".join(failures)
            evidence.extend(failures)
        elif forbidden or required:
            state = EvaluationState.PASS
            reason = "deterministic response checks matched expected behavior"
        else:
            state = EvaluationState.INDETERMINATE
            reason = "testcase has no deterministic expected-response checks"

        return EvaluationResult(
            testcase_id=testcase.id,
            target_id=response.target_id,
            run_id=run_id,
            result=state,
            evaluator=self.name,
            reason=reason,
            evidence=evidence,
            timestamp=datetime.now(UTC),
        )
