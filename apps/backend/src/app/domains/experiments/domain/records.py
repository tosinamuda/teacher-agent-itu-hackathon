"""Persistence-neutral records used by experiment application commands."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Protocol

from app.domains.experiments.domain.types import (
    ExecutionStatus,
    ExperimentLifecycleStatus,
    Hypothesis,
)
from app.shared.json_types import JsonObject


class ExperimentAdministrationRecord(Protocol):
    """Mutable experiment fields used by administration commands."""

    experiment_id: str
    teacher_workspace_id: uuid.UUID
    lesson_period_id: uuid.UUID | None
    plan_version_id: str | None
    focal_learner_ids: list[str] | None
    lifecycle_status: ExperimentLifecycleStatus
    ended_at: datetime | None
    ended_by: str | None
    is_sandbox: bool


class ExperimentPlanBindingRecord(Protocol):
    """Mutable experiment fields required to bind a lesson-plan version."""

    experiment_id: str
    lesson_period_id: uuid.UUID | None
    plan_version_id: str | None


class PlanVersionBindingRecord(Protocol):
    """Plan-version identity needed before an experiment binding is staged."""

    version_id: str
    plan_id: str


class LessonPlanBindingRecord(Protocol):
    """Plan identity and lesson ownership used to validate a binding."""

    plan_id: str
    lesson_period_id: uuid.UUID


class ExecutionRecord(Protocol):
    """One generation attempt, as every caller outside persistence sees it."""

    @property
    def id(self) -> uuid.UUID: ...

    @property
    def execution_id(self) -> str: ...

    @property
    def hypothesis(self) -> Hypothesis | str: ...

    # str until the callers still handing over an ORM row have their own operations;
    # every reader coerces with ``Hypothesis(...)``, which accepts both.

    @property
    def attempt_number(self) -> int: ...

    @property
    def status(self) -> ExecutionStatus: ...

    @property
    def runtime_snapshot(self) -> JsonObject | None: ...

    @property
    def error_message(self) -> str | None: ...

    @property
    def error_category(self) -> str | None: ...

    @property
    def created_at(self) -> datetime: ...

    @property
    def updated_at(self) -> datetime: ...
