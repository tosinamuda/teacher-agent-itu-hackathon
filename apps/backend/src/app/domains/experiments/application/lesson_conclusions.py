"""Concluding the lessons an ended experiment was run on."""

from __future__ import annotations

from collections.abc import Collection
from typing import Protocol


class LessonConclusions(Protocol):
    """Marks lessons concluded; their record is read-only from then."""

    async def conclude_where_no_experiment_is_active(
        self, plan_version_ids: Collection[str]
    ) -> None:
        """Conclude each plan version that no active experiment still runs on."""
        ...
