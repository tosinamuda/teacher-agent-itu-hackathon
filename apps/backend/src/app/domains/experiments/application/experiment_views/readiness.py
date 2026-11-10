"""Which phases of an experiment are ready to run, and how its executions roll up.

Pure policy over already-fetched rows: nothing here reads or writes.
"""

from __future__ import annotations

from collections.abc import Callable

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.experiments.api.schemas import (
    ExperimentFocalLearnerOptionResponse,
    ExperimentHypothesisSummaryResponse,
    ExperimentReadinessResponse,
)
from app.domains.experiments.application.experiment_context_service import ExperimentContext
from app.domains.experiments.domain import Hypothesis
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution

_READY_FLAG_BY_HYPOTHESIS: dict[Hypothesis, Callable[[ExperimentReadinessResponse], bool]] = {
    Hypothesis.H1: lambda r: r.h1_ready,
    Hypothesis.H2: lambda r: r.h2_ready,
}


def readiness_response(
    *,
    experiment: Experiment,
    context: ExperimentContext,
    selected_focal_learners: list[ExperimentFocalLearnerOptionResponse],
    base_pack_artefact_id: str | None,
    base_pack_approved: bool,
    h2_base_pack_artefact_id: str | None = None,
    h2_base_approved: bool = False,
    lesson_note_artefact_id: str | None = None,
    lesson_note_approved: bool = False,
) -> ExperimentReadinessResponse:
    """Compute the readiness flags for one experiment (h1/h2 ready + supporting flags).

    The base pack is the C4 condition-run artefact, the lesson's class pack the teacher
    reviews: *ready* once H1 has generated it and *approved* once the teacher has. H2
    personalises the first draw's C3 pack instead, so it gates on ``h2_base_approved``.
    H1 waits for the lesson note too: the conditions that read one are defined by it.
    """
    focal_learner_count = len(experiment.focal_learner_ids or [])
    selected_focal_count = len(selected_focal_learners)
    # No experiment plan yet → not approved → every downstream phase pending.
    lesson_approved = (
        context.plan_version is not None
        and context.plan_version.status == PlanVersionStatus.APPROVED
    )
    base_pack_ready = base_pack_artefact_id is not None
    learner_evidence_ready = context.diagnostic_count > 0
    h2_ready = (
        h2_base_approved
        and learner_evidence_ready
        and focal_learner_count > 0
        and focal_learner_count == selected_focal_count
    )
    return ExperimentReadinessResponse(
        lesson_approved=lesson_approved,
        baseline_selected=True,
        h1_ready=lesson_approved and lesson_note_approved,
        base_pack_ready=base_pack_ready,
        base_pack_approved=base_pack_approved,
        base_pack_artefact_id=base_pack_artefact_id,
        h2_base_pack_artefact_id=h2_base_pack_artefact_id,
        h2_base_approved=h2_base_approved,
        lesson_note_artefact_id=lesson_note_artefact_id,
        lesson_note_approved=lesson_note_approved,
        learner_evidence_ready=learner_evidence_ready,
        h2_ready=h2_ready,
    )


def hypothesis_summary_response(
    *,
    readiness: ExperimentReadinessResponse,
    executions: list[ExperimentExecution],
    hypothesis: Hypothesis,
) -> ExperimentHypothesisSummaryResponse:
    """Roll up one hypothesis' executions into the dashboard summary DTO."""
    filtered = [execution for execution in executions if execution.hypothesis == hypothesis.value]
    latest = filtered[0] if filtered else None
    return ExperimentHypothesisSummaryResponse(
        ready=_READY_FLAG_BY_HYPOTHESIS[hypothesis](readiness),
        execution_count=len(filtered),
        latest_execution_id=None if latest is None else latest.execution_id,
        latest_execution_status=None if latest is None else latest.status,
        latest_attempt_number=None if latest is None else latest.attempt_number,
    )
