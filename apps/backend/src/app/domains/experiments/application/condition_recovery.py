"""The stored-run operations a failed condition is retried through.

Separate from ``ExperimentStore.condition_runs``, which records a fresh grid and
nothing else. Recovery reads what an earlier attempt left behind and replaces
part of it, so it is a wider port and only the retry use case holds one.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol

from app.domains.experiments.domain.types import ConditionCode

if TYPE_CHECKING:
    from app.domains.experiments.infrastructure.models import ExperimentConditionRun
    from app.domains.experiments.review_pack_study.condition_runs.records import (
        CompletedConditionRun,
    )


class FailedConditionRunRecovery(Protocol):
    """The stored-run operations required to retry one failed condition family."""

    async def find(
        self,
        *,
        execution_db_id: uuid.UUID,
        condition_code: ConditionCode,
    ) -> ExperimentConditionRun | None: ...

    async def has_failures(
        self,
        *,
        execution_db_id: uuid.UUID,
    ) -> bool: ...

    async def replace_family(
        self,
        *,
        execution_db_id: uuid.UUID,
        condition_codes: Sequence[ConditionCode],
        records: Sequence[CompletedConditionRun],
    ) -> None: ...
