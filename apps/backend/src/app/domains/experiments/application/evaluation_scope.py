"""Experiment-owned records exposed to evaluation assignment use cases."""

from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationExperimentScope:
    id: uuid.UUID
    experiment_id: str
    lesson_period_id: uuid.UUID | None


@dataclass(frozen=True)
class EvaluationFocalCaseScope:
    focal_case_id: str
    student_id: str
    focal_case_type: str


@dataclass(frozen=True)
class EvaluationBundleScope:
    experiment: EvaluationExperimentScope
    execution_ids: tuple[uuid.UUID, ...]
    focal_cases: tuple[EvaluationFocalCaseScope, ...]

    @property
    def focal_case_ids(self) -> tuple[str, ...]:
        return tuple(case.focal_case_id for case in self.focal_cases)
