"""Pure derivation of the experiment workflow read-model + thin orchestrator.

This is the Python port of `apps/frontend/src/features/experiments/services/
workflow.ts`. Once the frontend switches to ``GET /experiments/{id}/workflow``,
the TS service collapses to presentation helpers and this module becomes the
single source of truth for "where is this experiment in the protocol".

The 7-phase / 18-item structure mirrors the settled design document:
1. Lesson plan                  (2 rows)
2. Generation — H1 (C0–C3)      (4 condition rows + 1 validation row)
3. Teacher governance           (1 row)
4. Assessment & learner state   (5 rows)
5. Personalisation — H2         (1 row)
6. Rating                       (3 rows: H1, H2, source audit)
7. Outputs                      (1 row)

Status derivation rules match the TS service exactly so the frontend swap
is a no-op behaviourally.
"""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field, replace
from datetime import datetime

from app.domains.evaluation.application.result_schemas import ExperimentStatistics
from app.domains.experiments.api.schemas import (
    ExperimentConditionRunResponse,
    ExperimentDetailResponse,
    ExperimentExecutionResponse,
    ExperimentReadinessResponse,
    ExperimentResponse,
)
from app.domains.experiments.api.workflow_schemas import (
    WorkflowItemResponse,
    WorkflowNextActionResponse,
    WorkflowPhaseResponse,
    WorkflowSnapshotResponse,
    WorkflowStatusKind,
    WorkflowSummaryResponse,
)
from app.domains.experiments.application.authorization import (
    ExperimentAccessReader,
    ExperimentAuthorization,
)
from app.shared.auth import Actor

H1_CONDITIONS = ("C0", "C1", "C2", "C3")

_DONE_STATUSES = re.compile(r"succeed|complete|done", re.IGNORECASE)
_FAILED_STATUSES = re.compile(r"fail|error|reject", re.IGNORECASE)
_IN_FLIGHT_STATUSES = re.compile(r"run|queue|pending|progress", re.IGNORECASE)


@dataclass(frozen=True)
class _WorkflowItem:
    """Internal mutable shape we build up before serialising to Pydantic.

    Frozen dataclass so we never accidentally mutate a row in place — the
    derivation reads as a sequence of small pure functions returning new
    items, which keeps the test fixtures simple.
    """

    id: str
    label: str
    status: WorkflowStatusKind
    count: str | None = None
    timestamp: datetime | None = None
    href: str | None = None
    action_label: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class _WorkflowPhase:
    id: str
    title: str
    description: str | None = None
    items: tuple[_WorkflowItem, ...] = field(default_factory=tuple)


# --- helpers over the ExperimentDetailResponse shape ---


def _hypothesis_executions(
    executions: list[ExperimentExecutionResponse], hypothesis: str
) -> list[ExperimentExecutionResponse]:
    return [execution for execution in executions if execution.hypothesis == hypothesis]


def _condition_runs(
    executions: list[ExperimentExecutionResponse], hypothesis: str, code: str
) -> list[ExperimentConditionRunResponse]:
    return [
        run
        for execution in _hypothesis_executions(executions, hypothesis)
        for run in execution.condition_runs
        if run.condition_code == code
    ]


def _latest_timestamp(
    executions: list[ExperimentExecutionResponse],
) -> datetime | None:
    """Most recent activity time across a set of executions.

    Backend's ``ExperimentExecutionResponse`` exposes ``updated_at`` /
    ``created_at`` (not the frontend's ``finished_at`` / ``started_at`` —
    those names live on the typescript ``ExperimentExecution`` shape, which
    is built from a different projection). Either backend field is a fine
    "last touched" signal for the workflow row timestamp.
    """
    candidates: list[datetime] = []
    for execution in executions:
        for candidate in (execution.updated_at, execution.created_at):
            if candidate is not None:
                candidates.append(candidate)
    return max(candidates) if candidates else None


def _condition_row(executions: list[ExperimentExecutionResponse], code: str) -> _WorkflowItem:
    """Status row for one H1 condition (C0-C3)."""
    runs = _condition_runs(executions, "H1", code)
    if not runs:
        return _WorkflowItem(id=f"cond-{code}", label=f"{code} generated", status="pending")
    succeeded = next((r for r in runs if _DONE_STATUSES.search(r.status)), None)
    if succeeded:
        return _WorkflowItem(
            id=f"cond-{code}",
            label=f"{code} generated",
            status="done",
            count=f"{len(runs)} attempts" if len(runs) > 1 else None,
        )
    failed = next((r for r in runs if _FAILED_STATUSES.search(r.status)), None)
    if failed:
        return _WorkflowItem(
            id=f"cond-{code}",
            label=f"{code} generated",
            status="failed",
            reason=failed.error_message or "Generation failed",
        )
    in_flight = next((r for r in runs if _IN_FLIGHT_STATUSES.search(r.status)), None)
    if in_flight:
        return _WorkflowItem(id=f"cond-{code}", label=f"{code} generated", status="in_progress")
    return _WorkflowItem(id=f"cond-{code}", label=f"{code} generated", status="pending")


def _c3_validation_row(
    executions: list[ExperimentExecutionResponse],
) -> _WorkflowItem:
    runs = _condition_runs(executions, "H1", "C3")
    attempts = len(runs)
    if attempts == 0:
        return _WorkflowItem(
            id="c3-validation",
            label="C3 validation passed / retried",
            status="pending",
        )
    passed = any(_DONE_STATUSES.search(r.status) for r in runs)
    if passed and attempts == 1:
        return _WorkflowItem(
            id="c3-validation",
            label="C3 validation passed",
            status="done",
            count="passed first try",
        )
    if passed:
        return _WorkflowItem(
            id="c3-validation",
            label="C3 validation passed after retry",
            status="done",
            count=f"{attempts} attempts",
        )
    return _WorkflowItem(
        id="c3-validation",
        label="C3 validation retrying",
        status="in_progress",
        count=f"{attempts} attempt{'' if attempts == 1 else 's'}",
    )


def _p0p1_row(executions: list[ExperimentExecutionResponse]) -> _WorkflowItem:
    p0 = _condition_runs(executions, "H2", "P0")
    p1 = _condition_runs(executions, "H2", "P1")
    total = len(p0) + len(p1)
    if total == 0:
        return _WorkflowItem(id="p0p1", label="P0/P1 generated", status="pending")
    done_p0 = sum(1 for r in p0 if _DONE_STATUSES.search(r.status))
    done_p1 = sum(1 for r in p1 if _DONE_STATUSES.search(r.status))
    done_count = done_p0 + done_p1
    status: WorkflowStatusKind = "done" if done_count == total else "in_progress"
    return _WorkflowItem(
        id="p0p1",
        label="P0 / P1 generated",
        status=status,
        count=f"{done_p0} P0 · {done_p1} P1",
    )


def _plan_phase(
    experiment: ExperimentResponse, readiness: ExperimentReadinessResponse
) -> _WorkflowPhase:
    has_plan = bool(experiment.plan_version_id)
    plan_href = "/lesson-plan" if has_plan else None
    return _WorkflowPhase(
        id="phase-plan",
        title="Lesson plan",
        description="The teacher-confirmed lesson plan everything else is derived from.",
        items=(
            _WorkflowItem(
                id="plan-created",
                label="Lesson plan created",
                status="done" if has_plan else "pending",
                href=plan_href,
                action_label="Preview plan",
            ),
            _WorkflowItem(
                id="plan-approved",
                label="Lesson plan approved / frozen",
                status="done" if readiness.lesson_approved else "pending",
                href=plan_href,
                action_label="Preview plan",
            ),
        ),
    )


def _condition_with_action(
    executions: list[ExperimentExecutionResponse],
    code: str,
    latest_h1_at: datetime | None,
) -> _WorkflowItem:
    """A condition row, with the right destination based on whether it's done.

    Done conditions preview the generated pack; pending/in-flight conditions
    open the Test tab so the researcher can trigger a (re)run.
    """
    base = _condition_row(executions, code)
    if base.status == "done":
        href, action = f"/{code.lower()}", f"Preview {code} pack"
    else:
        href, action = "/run", "Open test"
    return replace(base, href=href, action_label=action, timestamp=latest_h1_at)


def _h1_gen_phase(
    executions: list[ExperimentExecutionResponse], latest_h1_at: datetime | None
) -> _WorkflowPhase:
    return _WorkflowPhase(
        id="phase-h1-gen",
        title="Generation — H1 (C0–C3)",
        description=(
            "Tests curriculum alignment by comparing four conditioning regimes on the same lesson."
        ),
        items=(
            *(_condition_with_action(executions, code, latest_h1_at) for code in H1_CONDITIONS),
            replace(
                _c3_validation_row(executions),
                href="/run",
                action_label="Open test",
                timestamp=latest_h1_at,
            ),
        ),
    )


def _teacher_phase(readiness: ExperimentReadinessResponse) -> _WorkflowPhase:
    """Build the teacher-governance (C4) phase from the experiment's readiness.

    C4 is the classroom teacher's gate ONLY: they review + edit the C3 base pack
    (each edit logged via the pack revision loop) and approve it. ``base_pack_ready``
    means the C3 pack exists for review; ``base_pack_approved`` (their final accept)
    is the C4-ready signal. The researcher observes — they don't record C4.
    """
    if not readiness.base_pack_ready:
        status: WorkflowStatusKind = "pending"
        count = "awaiting the C3 base pack"
    elif readiness.base_pack_approved:
        status = "done"
        count = "approved by the teacher"
    else:
        status = "ready"
        count = "C3 pack ready — awaiting the teacher's review"
    return _WorkflowPhase(
        id="phase-teacher",
        title="Teacher governance",
        description=(
            "C4 — the classroom teacher reviews, edits and approves the C3 base "
            "pack. Their approval is the C4-ready signal."
        ),
        items=(
            _WorkflowItem(
                id="c4",
                label="C4 teacher decision",
                status=status,
                count=count,
                href="/results",
                action_label="View",
            ),
        ),
    )


def _assessment_phase(
    experiment: ExperimentResponse, readiness: ExperimentReadinessResponse
) -> _WorkflowPhase:
    learner_count = experiment.learner_count
    diagnostic_count = experiment.diagnostic_count
    focal_count = experiment.focal_learner_count
    assessment_href = "/assessment" if readiness.lesson_approved else None

    if diagnostic_count == 0:
        submissions_status: WorkflowStatusKind = "pending"
    elif diagnostic_count >= learner_count:
        submissions_status = "done"
    else:
        submissions_status = "in_progress"

    if focal_count > 0:
        focal_status: WorkflowStatusKind = "done"
    elif readiness.learner_evidence_ready:
        focal_status = "ready"
    else:
        focal_status = "pending"

    submissions_count = (
        f"{diagnostic_count} / {learner_count}" if learner_count > 0 else str(diagnostic_count)
    )
    learner_states_count = (
        f"{diagnostic_count} learner{'' if diagnostic_count == 1 else 's'} scored"
        if diagnostic_count > 0
        else None
    )
    focal_count_text = (
        f"{focal_count} learner{'' if focal_count == 1 else 's'}" if focal_count > 0 else None
    )

    return _WorkflowPhase(
        id="phase-assessment",
        title="Assessment & learner state",
        description=(
            "Exit-ticket diagnostic collects learner evidence, derives per-objective state, "
            "picks focal cases for H2."
        ),
        items=(
            _WorkflowItem(
                id="assessment-created",
                label="Exit assessment created",
                status="done" if readiness.lesson_approved else "pending",
                reason=None if readiness.lesson_approved else "lesson plan not yet approved",
                href=assessment_href,
                action_label="Preview assessment",
            ),
            _WorkflowItem(
                id="assessment-approved",
                label="Exit assessment approved",
                status="done" if readiness.lesson_approved else "pending",
                href=assessment_href,
                action_label="Preview assessment",
            ),
            _WorkflowItem(
                id="submissions",
                label="Student submissions",
                status=submissions_status,
                count=submissions_count,
            ),
            _WorkflowItem(
                id="learner-states",
                label="Learner states derived",
                status="done" if readiness.learner_evidence_ready else "pending",
                count=learner_states_count,
            ),
            _WorkflowItem(
                id="focal",
                label="Focal cases selected",
                status=focal_status,
                count=focal_count_text,
                href="/h2",
                action_label="Open H2 setup",
            ),
        ),
    )


def _h2_gen_phase(
    executions: list[ExperimentExecutionResponse], latest_h2_at: datetime | None
) -> _WorkflowPhase:
    return _WorkflowPhase(
        id="phase-h2-gen",
        title="Personalisation — H2",
        description="Tests P0 (base pack reused) vs P1 (personalised) on each focal learner.",
        items=(
            replace(
                _p0p1_row(executions),
                href="/run",
                action_label="Open test",
                timestamp=latest_h2_at,
            ),
        ),
    )


def _rating_row(item_id: str, label: str, packet_count: int, rating_count: int) -> _WorkflowItem:
    if packet_count == 0:
        status: WorkflowStatusKind = "pending"
    elif rating_count == 0:
        status = "ready"
    else:
        status = "in_progress"
    return _WorkflowItem(
        id=item_id,
        label=label,
        status=status,
        count=f"{rating_count} ratings · {packet_count} packets",
        href="/results",
        action_label="View progress",
    )


def _hypothesis_rating_count(hypothesis_stats: dict) -> int:
    """Pluck `n_ratings` from one of the dynamic h1/h2 JsonObject blobs."""
    return int(hypothesis_stats.get("n_ratings", 0))


def _rating_phase(
    stats: ExperimentStatistics, h1_packet_count: int, h2_packet_count: int
) -> _WorkflowPhase:
    audit = stats.source_audit
    h1_ratings = _hypothesis_rating_count(stats.h1)
    h2_ratings = _hypothesis_rating_count(stats.h2)
    if audit.n_items == 0:
        audit_status: WorkflowStatusKind = "pending"
    elif audit.n_ratings == 0:
        audit_status = "ready"
    else:
        audit_status = "in_progress"
    audit_count = f"{audit.n_ratings} ratings on {audit.n_items} items" if audit.n_items else None
    return _WorkflowPhase(
        id="phase-rating",
        title="Rating",
        description="Expert raters score H1, H2, and the separate source-grounding audit.",
        items=(
            _rating_row(
                "h1-rating", "H1 packets assigned / completed", h1_packet_count, h1_ratings
            ),
            _rating_row(
                "h2-rating", "H2 packets assigned / completed", h2_packet_count, h2_ratings
            ),
            _WorkflowItem(
                id="source-audit",
                label="Source audit sampled / completed",
                status=audit_status,
                count=audit_count,
                href="/results",
                action_label="View progress",
            ),
        ),
    )


def _outputs_phase(stats: ExperimentStatistics) -> _WorkflowPhase:
    has_ratings = _hypothesis_rating_count(stats.h1) + _hypothesis_rating_count(stats.h2) > 0
    return _WorkflowPhase(
        id="phase-outputs",
        title="Outputs",
        description=(
            "Downloadable artefacts for the thesis writeup — rendered packs, "
            "ratings CSV, audit pack PDF."
        ),
        items=(
            _WorkflowItem(
                id="exports",
                label="Exports ready",
                status="ready" if has_ratings else "pending",
                href="/results",
                action_label="Open Results",
            ),
        ),
    )


def _build_phases(
    detail: ExperimentDetailResponse, stats: ExperimentStatistics
) -> tuple[_WorkflowPhase, ...]:
    """Pure derivation: detail + stats → seven phases of workflow items."""
    experiment = detail.experiment
    executions = detail.executions
    readiness = experiment.readiness
    h1_executions = _hypothesis_executions(executions, "H1")
    h2_executions = _hypothesis_executions(executions, "H2")
    latest_h1_at = _latest_timestamp(h1_executions)
    latest_h2_at = _latest_timestamp(h2_executions)
    h1_packet_count = sum(len(execution.packets) for execution in h1_executions)
    h2_packet_count = sum(len(execution.packets) for execution in h2_executions)

    return (
        _plan_phase(experiment, readiness),
        _h1_gen_phase(executions, latest_h1_at),
        _teacher_phase(readiness),
        _assessment_phase(experiment, readiness),
        _h2_gen_phase(executions, latest_h2_at),
        _rating_phase(stats, h1_packet_count, h2_packet_count),
        _outputs_phase(stats),
    )


def _to_response_item(item: _WorkflowItem) -> WorkflowItemResponse:
    return WorkflowItemResponse(
        id=item.id,
        label=item.label,
        status=item.status,
        count=item.count,
        timestamp=item.timestamp,
        href=item.href,
        action_label=item.action_label,
        reason=item.reason,
    )


def _next_action(phases: tuple[_WorkflowPhase, ...]) -> WorkflowNextActionResponse | None:
    """First pending/ready item with an href, walking phases in declared order."""
    for phase in phases:
        for item in phase.items:
            if item.status in ("ready", "pending") and item.href:
                return WorkflowNextActionResponse(
                    label=f"{phase.title} — {item.label}", href=item.href
                )
    return None


def _attention_items(phases: tuple[_WorkflowPhase, ...]) -> list[WorkflowItemResponse]:
    """Rows that need researcher attention (currently: failed only)."""
    return [
        _to_response_item(item)
        for phase in phases
        for item in phase.items
        if item.status == "failed"
    ]


def build_snapshot(
    detail: ExperimentDetailResponse, stats: ExperimentStatistics
) -> WorkflowSnapshotResponse:
    """Pure entry point — takes already-fetched detail + stats, returns the snapshot.

    Kept side-effect-free so tests can drive it with crafted fixtures and
    every status transition is covered without touching the database.
    """
    phases = _build_phases(detail, stats)
    response_phases = [
        WorkflowPhaseResponse(
            id=phase.id,
            title=phase.title,
            description=phase.description,
            items=[_to_response_item(item) for item in phase.items],
        )
        for phase in phases
    ]
    total = sum(len(phase.items) for phase in phases)
    done = sum(1 for phase in phases for item in phase.items if item.status == "done")
    pct = round((done / total) * 100) if total else 0
    return WorkflowSnapshotResponse(
        experiment_id=detail.experiment.experiment_id,
        phases=response_phases,
        summary=WorkflowSummaryResponse(done=done, total=total, pct=pct),
        next_action=_next_action(phases),
        attention=_attention_items(phases),
    )


class ExperimentWorkflowQuery:
    """Thin orchestrator — fetches detail + statistics then calls `build_snapshot`.

    Holds no derivation logic itself (everything lives in pure module-level
    helpers above) so it's safe to swap, mock, or reuse from tasks/exports
    without dragging the database surface along.
    """

    def __init__(
        self,
        access: ExperimentAccessReader,
        detail_query: Callable[..., Awaitable[ExperimentDetailResponse]],
        statistics_query: Callable[[str], Awaitable[ExperimentStatistics]],
    ) -> None:
        self.access = access
        self.detail_query = detail_query
        self.statistics_query = statistics_query

    async def compute(self, actor: Actor, experiment_id: str) -> WorkflowSnapshotResponse:
        """Fetch detail + statistics for one experiment and build the snapshot.

        Mirrors the auth flow in ``GET /experiments/{id}`` — load via the
        ``ExperimentAuthorization`` gateway, then build the detail view, then
        compute statistics, then derive the workflow purely.
        """
        authorization = ExperimentAuthorization(self.access)
        experiment = await authorization.load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        detail = await self.detail_query(experiment=experiment)
        stats = await self.statistics_query(experiment_id)
        return build_snapshot(detail, stats)
