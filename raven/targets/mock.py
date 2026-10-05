from __future__ import annotations

from raven.schemas.result import TargetResponse
from raven.schemas.testcase import TestCase
from raven.targets.base import TargetAdapter


class MockTarget(TargetAdapter):
    """Deterministic local target used to prove RAVEN's orchestration path."""

    def __init__(self, target_id: str = "local-test-target") -> None:
        self.target_id = target_id

    async def execute(self, testcase: TestCase) -> TargetResponse:
        responses = {
            "controlled-disclosure": "I cannot provide the protected synthetic value.",
            "instruction-boundary": "I will follow the configured application policy.",
            "malformed-input": "The input was handled safely without changing policy boundaries.",
        }
        content = responses.get(
            testcase.category,
            "The mock target handled the testcase within its configured policy.",
        )
        return TargetResponse(
            testcase_id=testcase.id,
            target_id=self.target_id,
            content=content,
            metadata={"adapter": "mock"},
        )
