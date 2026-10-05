from __future__ import annotations

from abc import ABC, abstractmethod

from raven.schemas.result import TargetResponse
from raven.schemas.testcase import TestCase


class TargetAdapter(ABC):
    @abstractmethod
    async def execute(self, testcase: TestCase) -> TargetResponse:
        """Execute one testcase against an explicitly authorized target."""
