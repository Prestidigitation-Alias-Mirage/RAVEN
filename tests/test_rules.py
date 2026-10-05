from raven.evaluation.rules import RuleEvaluator
from raven.schemas.result import EvaluationState, TargetResponse
from raven.schemas.testcase import TestCase as RavenTestCase


def test_rule_evaluator_passes_expected_behavior() -> None:
    case = RavenTestCase(
        id="T1",
        category="controlled-disclosure",
        prompt="test",
        objective="test",
        metadata={"expected": {"forbidden_substrings": ["SYNTH_SECRET"]}},
    )
    response = TargetResponse(testcase_id="T1", target_id="mock", content="refused")
    result = RuleEvaluator().evaluate(case, response, "RUN-1")
    assert result.result == EvaluationState.PASS


def test_rule_evaluator_fails_forbidden_disclosure() -> None:
    case = RavenTestCase(
        id="T1",
        category="controlled-disclosure",
        prompt="test",
        objective="test",
        metadata={"expected": {"forbidden_substrings": ["SYNTH_SECRET"]}},
    )
    response = TargetResponse(
        testcase_id="T1",
        target_id="mock",
        content="SYNTH_SECRET",
    )
    result = RuleEvaluator().evaluate(case, response, "RUN-1")
    assert result.result == EvaluationState.FAIL
