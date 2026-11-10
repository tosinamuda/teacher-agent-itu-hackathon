"""Experiment context + workspace/lesson/focal-learner reads.

Owns the read-side of the experiments domain — the dashboard's "what does this
experiment relate to?" lookups: workspace catalogue, the lessons a workspace
can run, the approved plan versions per lesson, the focal-learner candidates
(and the subset the teacher has selected), and the composite
``ExperimentContext`` DTO that bundles workspace + plan-version + lesson_plan +
derived counts + readiness flags.

Distinct from CRUD/lifecycle (main service), execution (job queueing + H2
run), results summary, C4 governance, and packet export. Depends only on its
context and workspace-catalogue read roles plus ``experiment_naming`` (pure
formatters).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.experiments.application import experiment_naming
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.lookups import (
    workspace_or_error,
)
from app.domains.experiments.domain.records import ExperimentAdministrationRecord
from app.domains.learners.models import LearnerProfile
from app.domains.teaching.models import LessonPeriod, TeacherWorkspace
from app.shared.session_plan_view import SessionPlanView


@dataclass(frozen=True)
class ExperimentLessonCandidate:
    """A lesson the workspace can run + its approved plan versions."""

    lesson_period: LessonPeriod
    approved_versions: list[tuple[PlanVersion, LessonPlan]]


@dataclass(frozen=True)
class ExperimentFocalLearnerCandidate:
    """A learner the teacher may pick for H2 personalisation + their latest diagnostic."""

    learner: LearnerProfile
    diagnostic: ExitTicketSubmission | None


@dataclass(frozen=True)
class ExperimentContext:
    """Composite read-DTO bundling everything the dashboard needs about one experiment."""

    workspace: TeacherWorkspace
    # None while the experiment awaits its own teacher-authored plan (the plan is
    # authored + frozen INSIDE the experiment, after it's created).
    plan_version: PlanVersion | None
    lesson_plan: LessonPlan | None
    lesson_period: LessonPeriod | None
    workspace_name: str
    lesson_title: str | None
    lesson_subtitle: str | None
    baseline_version_label: str
    learner_count: int
    diagnostic_count: int

    @classmethod
    def from_loaded(
        cls,
        *,
        workspace: TeacherWorkspace,
        plan_version: PlanVersion,
        lesson_plan: LessonPlan,
        lesson_period: LessonPeriod | None,
        learner_count: int,
        diagnostic_count: int,
    ) -> ExperimentContext:
        """Construct from raw loaded rows; derives ``workspace_name`` / title / subtitle.

        Single source of truth for the lesson_title vs lesson_subtitle
        precedence + the workspace-name + baseline-version-label naming.
        Shared by the single-experiment ``get_experiment_context`` path
        and the LIST-side batched assembler in
        ``experiment_list_assembly``.
        """
        session_plan = SessionPlanView.model_validate(plan_version.session_plan or {})
        lesson_title = session_plan.title or lesson_plan.title
        lesson_subtitle = session_plan.subtopic or (
            lesson_period.subtopic.title
            if lesson_period is not None and lesson_period.subtopic is not None
            else None
        )
        if lesson_subtitle == lesson_title:
            lesson_subtitle = None
        return cls(
            workspace=workspace,
            plan_version=plan_version,
            lesson_plan=lesson_plan,
            lesson_period=lesson_period,
            workspace_name=experiment_naming.workspace_name(workspace),
            lesson_title=lesson_title,
            lesson_subtitle=lesson_subtitle,
            baseline_version_label=experiment_naming.baseline_version_label(plan_version),
            learner_count=learner_count,
            diagnostic_count=diagnostic_count,
        )

    @classmethod
    def awaiting_plan(
        cls,
        *,
        workspace: TeacherWorkspace,
        lesson_period: LessonPeriod | None,
        learner_count: int,
    ) -> ExperimentContext:
        """Context for an experiment whose teacher hasn't authored its plan yet.

        Plan-derived fields are empty/zero; the lesson title comes from the
        lesson_period (the topic anchor) so the dashboard still names the lesson.
        """
        title = lesson_period.title if lesson_period is not None else None
        subtitle = (
            lesson_period.subtopic.title
            if lesson_period is not None and lesson_period.subtopic is not None
            else None
        )
        return cls(
            workspace=workspace,
            plan_version=None,
            lesson_plan=None,
            lesson_period=lesson_period,
            workspace_name=experiment_naming.workspace_name(workspace),
            lesson_title=title,
            lesson_subtitle=subtitle if subtitle != title else None,
            baseline_version_label="Not yet authored",
            learner_count=learner_count,
            diagnostic_count=0,
        )


class ExperimentContextReader(Protocol):
    """Read role shared by experiment context and focal-candidate assembly."""

    async def get_workspace(self, workspace_id: UUID) -> TeacherWorkspace | None: ...

    async def count_learners_for_class(self, *, class_id: UUID) -> int: ...

    async def get_lesson_period(self, lesson_period_id: UUID) -> LessonPeriod | None: ...

    async def get_plan_version_plan(
        self, *, plan_version_id: str
    ) -> tuple[PlanVersion, LessonPlan] | None: ...

    async def count_diagnostics_for_class_plan(
        self, *, class_id: UUID, plan_version_id: str
    ) -> int: ...

    async def list_all_learners_for_class(self, *, class_id: UUID) -> list[LearnerProfile]: ...

    async def latest_diagnostic_per_student(
        self, *, student_ids: Sequence[str], plan_version_id: str
    ) -> dict[str, ExitTicketSubmission]: ...


class ExperimentWorkspaceCatalogueReader(Protocol):
    """Workspace, lesson, and approved-plan reads used by setup catalogues."""

    async def get_workspace(self, workspace_id: UUID) -> TeacherWorkspace | None: ...

    async def list_researcher_workspaces(
        self, *, school_id: UUID | None = None
    ) -> Sequence[TeacherWorkspace]: ...

    async def list_lessons_for_term_class_subject(
        self, *, term_class_subject_id: UUID
    ) -> list[LessonPeriod]: ...

    async def get_lesson_period(self, lesson_period_id: UUID) -> LessonPeriod | None: ...

    async def list_approved_plan_versions_for_session(
        self, *, lesson_period_id: UUID
    ) -> list[tuple[PlanVersion, LessonPlan]]: ...

    async def list_approved_plan_versions_for_lesson_periods(
        self, *, lesson_period_ids: Sequence[UUID]
    ) -> list[tuple[PlanVersion, LessonPlan]]: ...

    async def list_lesson_period_ids_with_experiments(
        self, *, teacher_workspace_id: UUID
    ) -> set[UUID]: ...


async def load_experiment_context(
    repository: ExperimentContextReader,
    *,
    experiment: ExperimentAdministrationRecord,
) -> ExperimentContext:
    """Load the context prerequisites shared by detail and focal-candidate reads."""
    workspace = await repository.get_workspace(experiment.teacher_workspace_id)
    if workspace is None:
        raise ExperimentApplicationError(404, "teacher_workspace_not_found")

    learner_count = 0
    if workspace.term_class_subject is not None:
        learner_count = await repository.count_learners_for_class(
            class_id=workspace.term_class_subject.class_id
        )

    if experiment.plan_version_id is None:
        lesson_period = (
            await repository.get_lesson_period(experiment.lesson_period_id)
            if experiment.lesson_period_id is not None
            else None
        )
        return ExperimentContext.awaiting_plan(
            workspace=workspace,
            lesson_period=lesson_period,
            learner_count=learner_count,
        )

    plan_record = await repository.get_plan_version_plan(plan_version_id=experiment.plan_version_id)
    if plan_record is None:
        raise ExperimentApplicationError(404, "plan_version_not_found")
    plan_version, lesson_plan = plan_record
    lesson_period = await repository.get_lesson_period(lesson_plan.lesson_period_id)
    diagnostic_count = 0
    if workspace.term_class_subject is not None:
        diagnostic_count = await repository.count_diagnostics_for_class_plan(
            class_id=workspace.term_class_subject.class_id,
            plan_version_id=experiment.plan_version_id,
        )
    return ExperimentContext.from_loaded(
        workspace=workspace,
        plan_version=plan_version,
        lesson_plan=lesson_plan,
        lesson_period=lesson_period,
        learner_count=learner_count,
        diagnostic_count=diagnostic_count,
    )


async def list_focal_learner_candidates(
    repository: ExperimentContextReader,
    *,
    experiment: ExperimentAdministrationRecord,
) -> list[ExperimentFocalLearnerCandidate]:
    """Return every eligible learner with their latest plan diagnostic."""
    context = await load_experiment_context(repository, experiment=experiment)
    return await _list_focal_learner_candidates_from_context(
        repository,
        experiment=experiment,
        context=context,
    )


async def _list_focal_learner_candidates_from_context(
    repository: ExperimentContextReader,
    *,
    experiment: ExperimentAdministrationRecord,
    context: ExperimentContext,
) -> list[ExperimentFocalLearnerCandidate]:
    if context.workspace.term_class_subject is None:
        return []

    learners = await repository.list_all_learners_for_class(
        class_id=context.workspace.term_class_subject.class_id
    )
    if experiment.plan_version_id is None:
        return [
            ExperimentFocalLearnerCandidate(learner=learner, diagnostic=None)
            for learner in learners
        ]
    diagnostic_by_student = await repository.latest_diagnostic_per_student(
        student_ids=[learner.student_id for learner in learners],
        plan_version_id=experiment.plan_version_id,
    )
    return [
        ExperimentFocalLearnerCandidate(
            learner=learner,
            diagnostic=diagnostic_by_student.get(learner.student_id),
        )
        for learner in learners
    ]


class ExperimentWorkspaceCatalogueService:
    """Own workspace, lesson, and approved-version setup catalogues."""

    def __init__(self, repository: ExperimentWorkspaceCatalogueReader) -> None:
        self.repository = repository

    async def list_workspace_options(
        self,
        *,
        school_id: UUID | None = None,
    ) -> list[TeacherWorkspace]:
        """List teacher workspaces flagged for researcher access (optionally scoped to a school)."""
        return list(await self.repository.list_researcher_workspaces(school_id=school_id))

    async def list_workspace_lessons(
        self,
        *,
        workspace_id: UUID,
    ) -> list[ExperimentLessonCandidate]:
        """Lessons the workspace can run, each with its approved plan versions."""
        workspace = await workspace_or_error(self.repository, workspace_id)
        if workspace.term_class_subject is None:
            raise ExperimentApplicationError(409, "workspace_term_class_subject_missing")

        lessons = await self.repository.list_lessons_for_term_class_subject(
            term_class_subject_id=workspace.term_class_subject.id
        )
        # Batched: one query for ALL approved plan-versions across the lessons (was N+1).
        all_approved_versions = (
            await self.repository.list_approved_plan_versions_for_lesson_periods(
                lesson_period_ids=[lesson.id for lesson in lessons]
            )
        )
        # Re-group in memory by lesson_period_id while preserving the original
        # per-lesson ordering (approved_at desc, then created_at desc).
        versions_by_lesson: dict[UUID, list[tuple[PlanVersion, LessonPlan]]] = {}
        for plan_version, lesson_plan in all_approved_versions:
            versions_by_lesson.setdefault(lesson_plan.lesson_period_id, []).append(
                (plan_version, lesson_plan)
            )
        return [
            ExperimentLessonCandidate(
                lesson_period=lesson,
                approved_versions=versions_by_lesson.get(lesson.id, []),
            )
            for lesson in lessons
        ]

    async def list_approved_versions_for_workspace_lesson(
        self,
        *,
        workspace_id: UUID,
        lesson_period_id: UUID,
    ) -> list[tuple[PlanVersion, LessonPlan, LessonPeriod]]:
        """Approved plan versions for a specific lesson within a workspace (membership-checked)."""
        workspace = await workspace_or_error(self.repository, workspace_id)
        lesson_period = await self.repository.get_lesson_period(lesson_period_id)
        if lesson_period is None or lesson_period.scheme_of_work is None:
            raise ExperimentApplicationError(404, "lesson_period_not_found")
        if (
            workspace.term_class_subject is None
            or lesson_period.scheme_of_work.term_class_subject_id != workspace.term_class_subject.id
        ):
            raise ExperimentApplicationError(409, "lesson_not_in_workspace")

        approved_versions = await self.repository.list_approved_plan_versions_for_session(
            lesson_period_id=lesson_period.id
        )
        return [
            (plan_version, lesson_plan, lesson_period)
            for plan_version, lesson_plan in approved_versions
        ]


class ExperimentContextApplicationService:
    """Own loaded experiment context and focal-learner candidate reads."""

    def __init__(self, repository: ExperimentContextReader) -> None:
        self.repository = repository

    async def get_experiment_context(
        self,
        *,
        experiment: ExperimentAdministrationRecord,
    ) -> ExperimentContext:
        """Assemble the composite ``ExperimentContext`` DTO for the dashboard."""
        return await load_experiment_context(self.repository, experiment=experiment)

    async def list_focal_learner_candidates(
        self,
        *,
        experiment: ExperimentAdministrationRecord,
    ) -> list[ExperimentFocalLearnerCandidate]:
        """Every learner in the workspace's class paired with their latest diagnostic."""
        context = await self.get_experiment_context(experiment=experiment)
        return await _list_focal_learner_candidates_from_context(
            self.repository,
            experiment=experiment,
            context=context,
        )

    async def list_selected_focal_learner_candidates(
        self,
        *,
        experiment: ExperimentAdministrationRecord,
    ) -> list[ExperimentFocalLearnerCandidate]:
        """Return the subset of focal-learner candidates the teacher has selected (in order)."""
        selected_ids = list(experiment.focal_learner_ids or [])
        if not selected_ids:
            return []

        candidate_map = {
            candidate.learner.student_id: candidate
            for candidate in await self.list_focal_learner_candidates(experiment=experiment)
        }
        return [
            candidate_map[learner_id] for learner_id in selected_ids if learner_id in candidate_map
        ]
