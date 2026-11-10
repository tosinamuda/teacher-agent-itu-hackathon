"""Loading a whole list of ``LoadedExperiment`` in a constant number of queries.

The detail endpoint loads one experiment's view inputs with four direct
queries. The list endpoint used to get its N by calling that same path in a
loop — about 10 queries per experiment, so ~110 round-trips for a workspace
with 11. ``load_experiment_list`` produces the identical ``LoadedExperiment``
values without the fan-out.

Three stages, in dependency order:

1. **Selection** — pure functions (``plan_version_ids``, ``lesson_period_ids``,
   ``class_ids``, ``class_plan_pairs``, ``focal_class_ids``,
   ``focal_students_by_plan``) answering "which ids does this read need?". They
   own every rule worth testing and touch no database, so
   ``tests/test_experiment_list_selection.py`` exercises them with plain objects.
2. **Reading** — ``_BatchedReads``, one method per round-trip, each a thin
   ``IN(...)`` call over a selection result.
3. **Joining** — ``experiment_list_assembly`` turns the id-keyed ``BatchedRows``
   back into one ``LoadedExperiment`` per experiment, in memory.

The reads run one after another, not concurrently: they share the repository's
session, and gathering two queries on one session raises
``IllegalStateChangeError``. Sequential is the constraint, not an oversight.

``tests/test_experiment_views_list_n_plus_one.py`` pins the resulting call
shape — each batched method called exactly once, the per-experiment methods
never — at N ∈ {1, 5, 20}. That test is the query inventory; a prose list here
would only drift out of date.
"""

from __future__ import annotations

import uuid
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, TypeAlias, TypeVar

from app.domains.experiments.application.experiment_list_assembly import (
    BatchedRows,
    loaded_experiment,
)
from app.domains.experiments.application.lesson_notes import LessonNotesReader, LessonNoteState
from app.domains.experiments.domain.types import ConditionCode

if TYPE_CHECKING:
    from app.domains.artefacts.core.infrastructure.models import Artefact
    from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
        LessonPlan,
        PlanVersion,
    )
    from app.domains.assessments.models import ExitTicketSubmission
    from app.domains.experiments.application.loaded_experiment import LoadedExperiment
    from app.domains.experiments.infrastructure.models import (
        Experiment,
        ExperimentConditionRun,
        ExperimentExecution,
    )
    from app.domains.learners.models import LearnerProfile
    from app.domains.teaching.models import LessonPeriod, TeacherWorkspace

    PlanPair: TypeAlias = tuple[PlanVersion, LessonPlan]
    Workspaces: TypeAlias = Mapping[uuid.UUID, TeacherWorkspace]

_Row = TypeVar("_Row")
_Key = TypeVar("_Key")


class ExperimentListReader(Protocol):
    """Batched rows required to assemble the experiment dashboard list."""

    async def list_workspaces_by_ids(
        self, workspace_ids: Sequence[uuid.UUID]
    ) -> list[TeacherWorkspace]: ...

    async def list_plan_version_plans_by_ids(
        self, plan_version_ids: Sequence[str]
    ) -> list[PlanPair]: ...

    async def list_lesson_periods_by_ids(
        self, lesson_period_ids: Sequence[uuid.UUID]
    ) -> list[LessonPeriod]: ...

    async def count_learners_per_class(
        self, *, class_ids: Sequence[uuid.UUID]
    ) -> dict[uuid.UUID, int]: ...

    async def count_diagnostics_per_class_plan(
        self, *, pairs: Sequence[tuple[uuid.UUID, str]]
    ) -> dict[tuple[uuid.UUID, str], int]: ...

    async def list_executions_for_experiments(
        self, *, experiment_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentExecution]: ...

    async def list_condition_runs_for_executions(
        self, *, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentConditionRun]: ...

    async def current_artefacts_by_condition_run(
        self, run_ids: Sequence[str]
    ) -> dict[str, Artefact]: ...

    async def list_all_learners_for_class(self, *, class_id: uuid.UUID) -> list[LearnerProfile]: ...

    async def latest_diagnostic_per_student(
        self, *, student_ids: Sequence[str], plan_version_id: str
    ) -> dict[str, ExitTicketSubmission]: ...


# ===== Selection: which ids does each layer need? (pure, no I/O) =====


def group_by(rows: Iterable[_Row], key: Callable[[_Row], _Key]) -> dict[_Key, list[_Row]]:
    """Rows bucketed under ``key``, each bucket keeping the order the rows arrived in."""
    grouped: dict[_Key, list[_Row]] = defaultdict(list)
    for row in rows:
        grouped[key(row)].append(row)
    return dict(grouped)


def class_of(experiment: Experiment, workspaces: Workspaces) -> uuid.UUID | None:
    """The class an experiment teaches, or ``None`` when its workspace is missing or unassigned."""
    workspace = workspaces.get(experiment.teacher_workspace_id)
    if workspace is None or workspace.term_class_subject is None:
        return None
    return workspace.term_class_subject.class_id


def plan_version_ids(experiments: Sequence[Experiment]) -> set[str]:
    """Plan versions to load. An experiment still awaiting its plan contributes none."""
    return {
        experiment.plan_version_id
        for experiment in experiments
        if experiment.plan_version_id is not None
    }


def lesson_period_ids(
    experiments: Sequence[Experiment], plans: Mapping[str, PlanPair]
) -> set[uuid.UUID]:
    """Lesson periods to load: each plan's, plus the plan-less experiments' own.

    An experiment awaiting its plan carries its lesson period directly, so the
    list view can still name the lesson before any plan exists.
    """
    from_plans = {
        plan.lesson_period_id for _, plan in plans.values() if plan.lesson_period_id is not None
    }
    from_experiments = {
        experiment.lesson_period_id
        for experiment in experiments
        if experiment.lesson_period_id is not None
    }
    return from_plans | from_experiments


def class_ids(experiments: Sequence[Experiment], workspaces: Workspaces) -> set[uuid.UUID]:
    """Classes to count rosters for — every experiment whose workspace resolves."""
    return {
        class_id
        for experiment in experiments
        if (class_id := class_of(experiment, workspaces)) is not None
    }


def class_plan_pairs(
    experiments: Sequence[Experiment], workspaces: Workspaces
) -> set[tuple[uuid.UUID, str]]:
    """(class, plan version) pairs to count diagnostics for.

    Plan-less experiments contribute none — they have nothing to diagnose against.
    """
    return {
        (class_id, experiment.plan_version_id)
        for experiment in experiments
        if experiment.plan_version_id is not None
        and (class_id := class_of(experiment, workspaces)) is not None
    }


def focal_class_ids(experiments: Sequence[Experiment], workspaces: Workspaces) -> set[uuid.UUID]:
    """Classes whose full roster a focal-learner selection needs.

    A selection is only actionable with a plan version to diagnose against, so
    experiments awaiting their plan are excluded here too.
    """
    return {
        class_id
        for experiment in experiments
        if experiment.focal_learner_ids
        and experiment.plan_version_id is not None
        and (class_id := class_of(experiment, workspaces)) is not None
    }


def focal_students_by_plan(
    experiments: Sequence[Experiment], workspaces: Workspaces
) -> dict[str, set[str]]:
    """Selected student ids grouped by the plan version their diagnostic belongs to.

    Experiments sharing a plan version merge into one bucket, which is what keeps
    the diagnostic reads bounded by distinct plans rather than by N.
    """
    by_plan: dict[str, set[str]] = defaultdict(set)
    for experiment in experiments:
        plan_version_id = experiment.plan_version_id
        if not experiment.focal_learner_ids or plan_version_id is None:
            continue
        if class_of(experiment, workspaces) is None:
            continue
        by_plan[plan_version_id].update(experiment.focal_learner_ids)
    return dict(by_plan)


# ===== Reading: one method, one round-trip =====


@dataclass(frozen=True)
class _BatchedReads:
    """The repository and experiment set every batched read needs.

    One instance per ``list_experiment_views`` request. Holding the pair here
    is what lets ``_read_all`` read as a chain of reads rather than
    re-threading the same arguments through every layer.
    """

    repository: ExperimentListReader
    notes: LessonNotesReader
    experiments: Sequence[Experiment]

    async def workspaces(self) -> dict[uuid.UUID, TeacherWorkspace]:
        ids = {experiment.teacher_workspace_id for experiment in self.experiments}
        rows = await self.repository.list_workspaces_by_ids(list(ids))
        return {row.id: row for row in rows}

    async def plans(self) -> dict[str, PlanPair]:
        rows = await self.repository.list_plan_version_plans_by_ids(
            list(plan_version_ids(self.experiments))
        )
        return {version.version_id: (version, plan) for version, plan in rows}

    async def lesson_periods(self, plans: Mapping[str, PlanPair]) -> dict[uuid.UUID, LessonPeriod]:
        rows = await self.repository.list_lesson_periods_by_ids(
            list(lesson_period_ids(self.experiments, plans))
        )
        return {row.id: row for row in rows}

    async def learner_counts(self, workspaces: Workspaces) -> dict[uuid.UUID, int]:
        return await self.repository.count_learners_per_class(
            class_ids=list(class_ids(self.experiments, workspaces))
        )

    async def diagnostic_counts(self, workspaces: Workspaces) -> dict[tuple[uuid.UUID, str], int]:
        return await self.repository.count_diagnostics_per_class_plan(
            pairs=list(class_plan_pairs(self.experiments, workspaces))
        )

    async def executions(self) -> list[ExperimentExecution]:
        return await self.repository.list_executions_for_experiments(
            experiment_db_ids=[experiment.id for experiment in self.experiments]
        )

    async def condition_runs(
        self, executions: Sequence[ExperimentExecution]
    ) -> list[ExperimentConditionRun]:
        return await self.repository.list_condition_runs_for_executions(
            execution_db_ids=[execution.id for execution in executions]
        )

    async def c4_packs(
        self, condition_runs: Sequence[ExperimentConditionRun]
    ) -> dict[str, Artefact]:
        """Each C4 run's current pack, resolved via ``artefacts.experiment_condition_run_id``."""
        run_ids = [
            run.experiment_condition_run_id
            for run in condition_runs
            if run.condition_code == ConditionCode.C4.value
        ]
        return await self.repository.current_artefacts_by_condition_run(run_ids)

    async def lesson_notes(self) -> dict[str, LessonNoteState]:
        return await self.notes.latest_lesson_notes(list(plan_version_ids(self.experiments)))

    async def focal_rosters(self, workspaces: Workspaces) -> dict[uuid.UUID, list[LearnerProfile]]:
        """One roster read per class holding a focal selection."""
        return {
            class_id: list(await self.repository.list_all_learners_for_class(class_id=class_id))
            for class_id in focal_class_ids(self.experiments, workspaces)
        }

    async def focal_diagnostics(
        self, workspaces: Workspaces
    ) -> dict[tuple[str, str], ExitTicketSubmission]:
        """One diagnostic read per plan version holding a focal selection."""
        latest: dict[tuple[str, str], ExitTicketSubmission] = {}
        for plan_id, students in focal_students_by_plan(self.experiments, workspaces).items():
            per_plan = await self.repository.latest_diagnostic_per_student(
                student_ids=list(students), plan_version_id=plan_id
            )
            for student_id, diagnostic in per_plan.items():
                latest[(student_id, plan_id)] = diagnostic
        return latest


async def load_experiment_list(
    *,
    repository: ExperimentListReader,
    lesson_notes: LessonNotesReader,
    experiments: Sequence[Experiment],
) -> list[LoadedExperiment]:
    """Load every experiment's view inputs in a constant number of queries.

    Experiments whose workspace or plan version is missing are dropped, which
    is what the LIST view does instead of failing the whole call — so the
    result may be shorter than ``experiments``.
    """
    rows = await _read_all(repository=repository, notes=lesson_notes, experiments=experiments)
    return [
        loaded
        for experiment in experiments
        if (loaded := loaded_experiment(experiment, rows)) is not None
    ]


async def _read_all(
    *,
    repository: ExperimentListReader,
    notes: LessonNotesReader,
    experiments: Sequence[Experiment],
) -> BatchedRows:
    """Issue every batched read once, in dependency order.

    One line per round-trip: the lesson periods key off the plans, the condition
    runs off the executions, and the packs off the runs.
    """
    read = _BatchedReads(repository=repository, notes=notes, experiments=experiments)
    workspaces = await read.workspaces()
    plans = await read.plans()
    lesson_periods = await read.lesson_periods(plans)
    learner_counts = await read.learner_counts(workspaces)
    diagnostic_counts = await read.diagnostic_counts(workspaces)
    executions = await read.executions()
    condition_runs = await read.condition_runs(executions)
    c4_packs = await read.c4_packs(condition_runs)
    lesson_notes = await read.lesson_notes()
    rosters = await read.focal_rosters(workspaces)
    diagnostics = await read.focal_diagnostics(workspaces)

    return BatchedRows(
        workspaces_by_id=workspaces,
        plan_version_plans_by_id=plans,
        lesson_periods_by_id=lesson_periods,
        learner_count_by_class=learner_counts,
        diagnostic_count_by_class_plan=diagnostic_counts,
        executions_by_experiment=group_by(executions, lambda row: row.experiment_db_id),
        condition_runs_by_execution=group_by(condition_runs, lambda row: row.execution_db_id),
        artefacts_by_condition_run=c4_packs,
        lesson_notes_by_plan=lesson_notes,
        learners_by_class=rosters,
        diagnostic_by_student_plan=diagnostics,
    )
