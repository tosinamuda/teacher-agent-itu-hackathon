"""Render one resolved experiment to the dashboard's ``ExperimentResponse``.

Mapping only — every value is already in hand by the time these are called.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from app.domains.experiments.api.schemas import (
    ExperimentFocalLearnerOptionResponse,
    ExperimentReadinessResponse,
    ExperimentResponse,
)
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContext,
    ExperimentFocalLearnerCandidate,
)
from app.domains.experiments.application.experiment_views.readiness import (
    hypothesis_summary_response,
)
from app.domains.experiments.domain import ExperimentLifecycleStatus, Hypothesis
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution

_T = TypeVar("_T")
_R = TypeVar("_R")


def _opt(value: _T | None, project: Callable[[_T], _R]) -> _R | None:
    """Apply ``project`` when ``value`` is present, else ``None`` (safe navigation)."""
    return None if value is None else project(value)


def focal_candidate_response(
    candidate: ExperimentFocalLearnerCandidate,
) -> ExperimentFocalLearnerOptionResponse:
    """Render a focal-learner candidate to the API option DTO."""
    return ExperimentFocalLearnerOptionResponse(
        learner_id=candidate.learner.student_id,
        learner_name=candidate.learner.full_name,
        latest_diagnostic_id=(
            candidate.diagnostic.diagnostic_id if candidate.diagnostic is not None else None
        ),
        has_evidence=candidate.diagnostic is not None,
        latest_submitted_at=(
            candidate.diagnostic.created_at if candidate.diagnostic is not None else None
        ),
    )


def assemble_experiment_response(
    *,
    experiment: Experiment,
    context: ExperimentContext,
    executions: list[ExperimentExecution],
    readiness: ExperimentReadinessResponse,
) -> ExperimentResponse:
    """Assemble the big ``ExperimentResponse`` from the resolved context + executions."""
    tcs = context.workspace.term_class_subject
    classroom = _opt(tcs, lambda t: t.classroom)
    school = _opt(classroom, lambda c: c.school)
    teacher = context.workspace.teacher
    course = _opt(tcs, lambda t: t.course)
    latest_execution = executions[0] if executions else None
    hypothesis_value = _opt(latest_execution, lambda e: Hypothesis(e.hypothesis))
    return ExperimentResponse(
        experiment_id=experiment.experiment_id,
        experiment_code=experiment.experiment_code,
        teacher_workspace_id=experiment.teacher_workspace_id,
        workspace_name=context.workspace_name,
        teacher_id=_opt(teacher, lambda t: t.id),
        teacher_name=_opt(teacher, lambda t: t.full_name),
        school_id=_opt(school, lambda s: s.id),
        school_name=_opt(school, lambda s: s.name),
        school_code=_opt(school, lambda s: s.code),
        class_id=_opt(classroom, lambda c: c.id),
        class_name=_opt(classroom, lambda c: c.name),
        subject_name=_opt(course, lambda c: c.subject.name if c.subject is not None else None),
        subject_code=_opt(course, lambda c: c.subject.code if c.subject is not None else None),
        grade_level=_opt(
            course, lambda c: c.grade_level.name if c.grade_level is not None else None
        ),
        term=_opt(tcs, lambda t: t.term),
        academic_year=_opt(tcs, lambda t: t.year),
        plan_version_id=experiment.plan_version_id,
        baseline_version_label=context.baseline_version_label,
        baseline_approved_by=getattr(context.plan_version, "approved_by", None),
        lesson_period_id=_opt(context.lesson_period, lambda lp: lp.id),
        lesson_title=context.lesson_title,
        lesson_subtitle=context.lesson_subtitle,
        learner_count=context.learner_count,
        diagnostic_count=context.diagnostic_count,
        focal_learner_count=len(experiment.focal_learner_ids or []),
        readiness=readiness,
        h1_summary=hypothesis_summary_response(
            readiness=readiness, executions=executions, hypothesis=Hypothesis.H1
        ),
        h2_summary=hypothesis_summary_response(
            readiness=readiness, executions=executions, hypothesis=Hypothesis.H2
        ),
        hypothesis=hypothesis_value,
        status=latest_execution.status if latest_execution is not None else "created",
        lifecycle_status=(
            getattr(experiment, "lifecycle_status", None) or ExperimentLifecycleStatus.ACTIVE
        ),
        ended_at=getattr(experiment, "ended_at", None),
        ended_by=getattr(experiment, "ended_by", None),
        is_sandbox=bool(getattr(experiment, "is_sandbox", False)),
        execution_count=len(executions),
        latest_execution_status=_opt(latest_execution, lambda e: e.status),
        created_at=experiment.created_at,
    )


def matches_experiment_query(experiment: ExperimentResponse, query: str) -> bool:
    """Whether a normalised search query matches one of the experiment's display fields."""
    normalized = query.strip().lower()
    haystack = " ".join(
        value.lower()
        for value in [
            experiment.experiment_code,
            experiment.lesson_title or "",
            experiment.lesson_subtitle or "",
            experiment.workspace_name or "",
            experiment.school_name or "",
            experiment.class_name or "",
            experiment.teacher_name or "",
            experiment.subject_name or "",
            experiment.baseline_version_label or "",
        ]
        if value
    )
    return normalized in haystack
