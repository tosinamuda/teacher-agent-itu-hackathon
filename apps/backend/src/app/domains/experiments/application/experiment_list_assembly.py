"""Joining batch-loaded rows back into one experiment's ``LoadedExperiment``.

``experiment_list_loader`` fetches every related row for N experiments in a
constant number of queries and hands the result over as ``BatchedRows`` — one
id-keyed map per table, which is the shape a batched read produces but not the
shape a view wants. This module does the join: ``loaded_experiment`` turns
``(one experiment, all the rows)`` into the same ``LoadedExperiment`` the detail
endpoint builds from four direct queries.

Pure and synchronous throughout — no session, no repository, no awaits. That is
the point of the batching: pay for the data once, then assemble N views in
memory.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeAlias

from app.domains.experiments.application.experiment_context_service import (
    ExperimentContext,
    ExperimentFocalLearnerCandidate,
)
from app.domains.experiments.application.h2_base_pack import first_draw_c3_run
from app.domains.experiments.application.lesson_notes import LessonNoteState
from app.domains.experiments.application.loaded_experiment import LoadedExperiment
from app.domains.experiments.domain import Hypothesis
from app.domains.experiments.domain.types import ConditionCode

if TYPE_CHECKING:
    from app.domains.artefacts.core.infrastructure.models import Artefact
    from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
        LessonPlan,
        PlanVersion,
    )
    from app.domains.assessments.models import ExitTicketSubmission
    from app.domains.experiments.infrastructure.models import (
        Experiment,
        ExperimentConditionRun,
        ExperimentExecution,
    )
    from app.domains.learners.models import LearnerProfile
    from app.domains.teaching.models import LessonPeriod, TeacherWorkspace

    PlanPair: TypeAlias = tuple[PlanVersion, LessonPlan]


@dataclass
class BatchedRows:
    """Every related row for a set of experiments, indexed for lookup.

    One map per batched read — that one-to-one is why there are ten of them, and
    the ``*_by_*`` names say which id each is keyed on. Where a lookup takes a
    composite key or an optional id, ask the method rather than reaching into
    the map: the key shape and the empty-case default belong here, not at every
    call site.
    """

    workspaces_by_id: dict[uuid.UUID, TeacherWorkspace]
    plan_version_plans_by_id: dict[str, PlanPair]
    lesson_periods_by_id: dict[uuid.UUID, LessonPeriod]
    learner_count_by_class: dict[uuid.UUID, int]
    diagnostic_count_by_class_plan: dict[tuple[uuid.UUID, str], int]
    executions_by_experiment: dict[uuid.UUID, list[ExperimentExecution]] = field(
        default_factory=dict
    )
    condition_runs_by_execution: dict[uuid.UUID, list[ExperimentConditionRun]] = field(
        default_factory=dict
    )
    # Keyed by condition-run business id, resolved via the artefact-side back-pointer.
    artefacts_by_condition_run: dict[str, Artefact] = field(default_factory=dict)
    lesson_notes_by_plan: dict[str, LessonNoteState] = field(default_factory=dict)
    learners_by_class: dict[uuid.UUID, list[LearnerProfile]] = field(default_factory=dict)
    diagnostic_by_student_plan: dict[tuple[str, str], ExitTicketSubmission] = field(
        default_factory=dict
    )

    def lesson_period(self, lesson_period_id: uuid.UUID | None) -> LessonPeriod | None:
        """The lesson period, tolerating the absent id of an experiment with no plan."""
        if lesson_period_id is None:
            return None
        return self.lesson_periods_by_id.get(lesson_period_id)

    def learner_count(self, class_id: uuid.UUID | None) -> int:
        """Roster size — zero for a workspace with no class assigned."""
        return 0 if class_id is None else self.learner_count_by_class.get(class_id, 0)

    def diagnostic_count(self, class_id: uuid.UUID | None, plan_version_id: str) -> int:
        """How many of the class have sat this plan's diagnostic."""
        if class_id is None:
            return 0
        return self.diagnostic_count_by_class_plan.get((class_id, plan_version_id), 0)

    def roster(self, class_id: uuid.UUID | None) -> list[LearnerProfile]:
        """The class's learners — empty when the class had no focal selection to batch."""
        return [] if class_id is None else self.learners_by_class.get(class_id, [])

    def latest_diagnostic(
        self, student_id: str, plan_version_id: str | None
    ) -> ExitTicketSubmission | None:
        """This student's most recent diagnostic against the plan, if they sat one."""
        if plan_version_id is None:
            return None
        return self.diagnostic_by_student_plan.get((student_id, plan_version_id))


def loaded_experiment(experiment: Experiment, rows: BatchedRows) -> LoadedExperiment | None:
    """Join one experiment against the batched rows.

    Returns ``None`` when the workspace or the plan version is missing from the
    batch — the same conditions the single-experiment path raises
    ``ExperimentApplicationError`` for, but in the LIST view we drop the
    experiment from the result rather than failing the whole call.
    """
    workspace = rows.workspaces_by_id.get(experiment.teacher_workspace_id)
    if workspace is None:
        return None
    context = _context(experiment, rows, workspace)
    if context is None:
        return None
    return LoadedExperiment(
        experiment=experiment,
        context=context,
        executions=list(rows.executions_by_experiment.get(experiment.id, [])),
        focal_learners=_focal_learners(experiment, rows, workspace),
        base_pack=_base_pack(experiment, rows),
        h2_base_pack=_h2_base_pack(experiment, rows),
        lesson_note=rows.lesson_notes_by_plan.get(experiment.plan_version_id or ""),
    )


def _context(
    experiment: Experiment, rows: BatchedRows, workspace: TeacherWorkspace
) -> ExperimentContext | None:
    """The dashboard context DTO, or ``None`` when the plan version is missing."""
    class_id = _class_id(workspace)
    learner_count = rows.learner_count(class_id)

    # Awaiting its plan — keep it in the list in the "no plan yet" shape.
    if experiment.plan_version_id is None:
        return ExperimentContext.awaiting_plan(
            workspace=workspace,
            lesson_period=rows.lesson_period(experiment.lesson_period_id),
            learner_count=learner_count,
        )

    plan_pair = rows.plan_version_plans_by_id.get(experiment.plan_version_id)
    if plan_pair is None:
        return None
    plan_version, lesson_plan = plan_pair
    return ExperimentContext.from_loaded(
        workspace=workspace,
        plan_version=plan_version,
        lesson_plan=lesson_plan,
        lesson_period=rows.lesson_period(lesson_plan.lesson_period_id),
        learner_count=learner_count,
        diagnostic_count=rows.diagnostic_count(class_id, experiment.plan_version_id),
    )


def _focal_learners(
    experiment: Experiment, rows: BatchedRows, workspace: TeacherWorkspace
) -> list[ExperimentFocalLearnerCandidate]:
    """The selected focal learners paired with their latest diagnostics.

    Mirrors ``ExperimentContextApplicationService.list_selected_focal_learner_candidates``.
    Empty when nothing is selected, or when the class roster wasn't batched.
    """
    if not experiment.focal_learner_ids:
        return []
    roster = {learner.student_id: learner for learner in rows.roster(_class_id(workspace))}
    return [
        ExperimentFocalLearnerCandidate(
            learner=roster[student_id],
            diagnostic=rows.latest_diagnostic(student_id, experiment.plan_version_id),
        )
        for student_id in experiment.focal_learner_ids
        if student_id in roster
    ]


def _base_pack(experiment: Experiment, rows: BatchedRows) -> Artefact | None:
    """The C4 base-pack artefact (any status) across this experiment's H1 runs.

    Mirrors ``c4_base_pack.current_c4_artefact`` for the
    batched path. The caller derives ``base_pack_ready`` (artefact present) and
    ``base_pack_approved`` (artefact review status) from it.
    """
    for execution in rows.executions_by_experiment.get(experiment.id, []):
        if execution.hypothesis != Hypothesis.H1.value:
            continue
        for run in rows.condition_runs_by_execution.get(execution.id, []):
            if run.condition_code != ConditionCode.C4.value:
                continue
            artefact = rows.artefacts_by_condition_run.get(run.experiment_condition_run_id)
            if artefact is not None:
                return artefact
    return None


def _h2_base_pack(experiment: Experiment, rows: BatchedRows) -> Artefact | None:
    """H2's base, the first draw's C3 pack (any status); mirrors ``first_draw_c3_artefact``."""
    run = first_draw_c3_run(
        list(rows.executions_by_experiment.get(experiment.id, [])),
        rows.condition_runs_by_execution,
    )
    return (
        None
        if run is None
        else rows.artefacts_by_condition_run.get(run.experiment_condition_run_id)
    )


def _class_id(workspace: TeacherWorkspace) -> uuid.UUID | None:
    """The class this workspace teaches, or ``None`` when it has no subject assigned."""
    if workspace.term_class_subject is None:
        return None
    return workspace.term_class_subject.class_id
