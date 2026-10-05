import pytest

from raven.schemas.testcase import TestCase as RavenTestCase
from raven.targets.mock import MockTarget


@pytest.mark.asyncio
async def test_mock_target_is_deterministic() -> None:
    target = MockTarget()
    case = RavenTestCase(
        id="T1",
        category="instruction-boundary",
        prompt="test",
        objective="test",
    )
    response = await target.execute(case)
    assert response.target_id == "local-test-target"
    assert "configured application policy" in response.content
