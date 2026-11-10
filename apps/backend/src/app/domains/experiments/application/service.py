from __future__ import annotations

from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.retry import commit_with_unique_retry

if TYPE_CHECKING:
    from collections.abc import Sequence

    from app.domains.assessments.classwork_schemas import (
        ClassworkCoverageResponse,
        ManualClassworkItem,
    )

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.experiments.application import experiment_naming, lookups
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.execution_launch import LaunchExecutionInput
from app.domains.experiments.application.experiment_authoring import (
    bind_experiment_plan_version,
)
from app.domains.experiments.application.experiment_authoring_store import (
    ExperimentAuthoringStore,
)
from app.domains.experiments.application.filters import ExperimentListFilters
from app.domains.experiments.application.lesson_ownership import assert_actor_owns_lesson
from app.domains.experiments.domain import Hypothesis
from app.domains.experiments.infrastructure.models import (
    Experiment,
)
from app.domains.teaching.models import TeacherWorkspace
from app.domains.teaching.models.syllabus import LessonPeriod
from app.shared.auth import ROLE_TEACHER, Actor
from app.shared.ids import PublicIdPrefix, new_public_id


class InvestigationIdentity(Protocol):
    id: UUID


class PlanStatusRecord(Protocol):
    status: PlanVersionStatus


class PlanIdentity(Protocol):
    plan_id: str


class ExperimentApplicationQueries(Protocol):
    """Reads used by experiment setup and teacher preparation commands."""

    async def get_investigation(self, investigation_id: str) -> InvestigationIdentity | None: ...

    async def get_workspace(self, workspace_id: UUID) -> TeacherWorkspace | None: ...

    async def get_lesson_period(self, lesson_period_id: UUID) -> LessonPeriod | None: ...

    async def next_experiment_code_sequence(self, *, code_prefix: str) -> int: ...

    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def get_plan_version(self, plan_version_id: str) -> PlanStatusRecord | None: ...

    async def approved_lesson_note(self, plan_version_id: str) -> object | None: ...

    async def get_plan_version_plan(
        self, *, plan_version_id: str
    ) -> tuple[object, PlanIdentity] | None: ...

    async def list_experiments(self, *, filters: ExperimentListFilters) -> Sequence[Experiment]: ...


class ReviewNoteLauncher(Protocol):
    """The launch operation, as the review-note flow calls it."""

    async def __call__(self, request: LaunchExecutionInput) -> object: ...


class ExperimentApplicationService:
    def __init__(self, repository: ExperimentApplicationQueries) -> None:
        self.repository = repository

    async def create_experiment(
        self,
        *,
        db: AsyncSession,
        investigation_id: str,
        teacher_workspace_id: UUID,
        lesson_period_id: UUID,
    ) -> Experiment:
        """Create an experiment for a (workspace, lesson) inside a study.

        Always creates a new experiment — multiple experiments per lesson (reruns
        and variants) are first-class, so this is not idempotent. The parent study
        is required; the experiment is created against the lesson it studies, and
        its own plan is authored + frozen by the assigned teacher afterwards
        (``draft_experiment_plan`` / ``freeze_experiment_plan``), which is what
        triggers C0–C3.
        """
        investigation = await self.repository.get_investigation(investigation_id)
        if investigation is None:
            raise ExperimentApplicationError(404, "investigation_not_found")
        workspace = await lookups.workspace_or_error(self.repository, teacher_workspace_id)
        lesson_period = await lookups.resolve_lesson_period(self.repository, lesson_period_id)
        if lesson_period is None:
            raise ExperimentApplicationError(404, "lesson_period_not_found")
        self._ensure_lesson_matches_workspace(workspace=workspace, lesson_period=lesson_period)

        code_prefix = experiment_naming.experiment_code_prefix(workspace)
        # Capture scalar FK values BEFORE the retry loop. commit_with_unique_retry
        # rolls back on a code collision, which expires every ORM object in the
        # session; re-reading ``investigation.id`` inside the retried closure would
        # trigger an implicit lazy-load and raise MissingGreenlet under async.
        investigation_db_id = investigation.id

        async def _build() -> Experiment:
            # Re-derive the sequence on every attempt: under concurrency two
            # callers read the same MAX and mint the same experiment_code; the
            # loser hits the unique index and retries against the now-committed
            # max (commit_with_unique_retry owns the rollback + retry).
            sequence = await self.repository.next_experiment_code_sequence(code_prefix=code_prefix)
            experiment = Experiment(
                experiment_id=new_public_id(PublicIdPrefix.EXPERIMENT),
                experiment_code=f"{code_prefix}-{sequence:03d}",
                investigation_db_id=investigation_db_id,
                teacher_workspace_id=teacher_workspace_id,
                lesson_period_id=lesson_period_id,
                plan_version_id=None,
                focal_learner_ids=[],
            )
            db.add(experiment)
            return experiment

        experiment = await commit_with_unique_retry(db, _build, conflict_token="experiment_code")
        await db.refresh(experiment)
        return experiment

    async def check_plan_authoring(
        self, *, db: AsyncSession, experiment_id: str, actor: Actor
    ) -> None:
        """Refuse now what drafting the experiment's plan would refuse.

        The draft itself runs as a job; only an experiment with a lesson, authored by a
        teacher of that class (a manager bypasses), is ever queued.
        """
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if experiment.lesson_period_id is None:
            raise ExperimentApplicationError(409, "experiment_lesson_missing")
        await assert_actor_owns_lesson(
            db, actor=actor, lesson_period_id=experiment.lesson_period_id
        )

    async def draft_experiment_plan(
        self,
        *,
        db: AsyncSession,
        authoring_store: ExperimentAuthoringStore,
        experiment_id: str,
    ) -> str:
        """Draft the experiment's OWN plan and bind it; returns the new plan version's id.

        Mints a FRESH ``LessonPlan`` + ``PlanVersion`` (marked
        ``source_type="experiment_generated"``) on the experiment's lesson, via the same
        drafting pipeline the teacher uses in production, then binds it.
        """
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if experiment.lesson_period_id is None:
            raise ExperimentApplicationError(409, "experiment_lesson_missing")

        from app.domains.artefacts.types.lesson_plan.api.schemas import PlanGenerateRequest
        from app.domains.artefacts.types.lesson_plan.deps import (
            lesson_plan_service,
        )

        plan_service = lesson_plan_service(db)
        result = await plan_service.generate(
            PlanGenerateRequest(session_id=str(experiment.lesson_period_id)),
            source_type="experiment_generated",
        )
        await bind_experiment_plan_version(
            authoring_store,
            experiment_id=experiment_id,
            plan_version_id=result.version_id,
        )
        return result.version_id

    async def author_experiment_plan_manual(
        self,
        *,
        db: AsyncSession,
        authoring_store: ExperimentAuthoringStore,
        experiment_id: str,
        actor: Actor,
        session_plan_content: dict,
        original_document_attachment_id: str | None = None,
    ) -> Experiment:
        """Author the experiment's OWN plan from hand-entered content (FD-01).

        The manual counterpart of :meth:`draft_experiment_plan`: instead of the
        LLM drafting pipeline, the teacher/researcher supplies the plan content,
        which is validated against ``SessionPlan`` and bound to the experiment.
        Ownership is asserted here (a research-manager bypasses), so the inner
        create runs without re-checking. A validation gap surfaces as 422.
        """
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if experiment.lesson_period_id is None:
            raise ExperimentApplicationError(409, "experiment_lesson_missing")
        await assert_actor_owns_lesson(
            db, actor=actor, lesson_period_id=experiment.lesson_period_id
        )

        from app.domains.artefacts.types.lesson_plan.application.errors import (
            PlanValidationError,
        )
        from app.domains.artefacts.types.lesson_plan.deps import (
            lesson_plan_service,
        )

        plan_service = lesson_plan_service(db)
        try:
            result = await plan_service.create_manual(
                session_id=str(experiment.lesson_period_id),
                session_plan_content=session_plan_content,
                teacher_id=str(actor.teacher_id) if actor.teacher_id else None,
                owner_teacher_id=None,
                source_type="experiment_manual",
                original_document_attachment_id=original_document_attachment_id,
            )
        except PlanValidationError as error:
            raise ExperimentApplicationError(422, str(error.detail)) from None
        await bind_experiment_plan_version(
            authoring_store,
            experiment_id=experiment_id,
            plan_version_id=result.version_id,
        )
        return await self.get_experiment(experiment_id=experiment_id)

    async def author_experiment_classwork_manual(
        self,
        *,
        db: AsyncSession,
        experiment_id: str,
        actor: Actor,
        items: Sequence[ManualClassworkItem],
    ) -> ClassworkCoverageResponse:
        """Enter the experiment lesson's real classwork by hand (FD-02).

        The classwork counterpart of :meth:`author_experiment_plan_manual`: persists
        the items against the experiment's frozen plan version and returns the
        coverage report. Requires the plan to be authored (409 otherwise) and asserts
        the teacher owns the lesson (a research-manager bypasses). A validation gap or
        a frozen/answered assessment surfaces with the assessment service's status.
        """
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if experiment.lesson_period_id is None:
            raise ExperimentApplicationError(409, "experiment_lesson_missing")
        if experiment.plan_version_id is None:
            raise ExperimentApplicationError(409, "experiment_plan_not_authored")
        await assert_actor_owns_lesson(
            db, actor=actor, lesson_period_id=experiment.lesson_period_id
        )

        from app.domains.assessments.application.classwork_service import (
            ClassworkApplicationService,
        )
        from app.domains.assessments.application.service import AssessmentApplicationError

        try:
            return await ClassworkApplicationService().create_manual_classwork(
                db=db, plan_version_id=experiment.plan_version_id, items=items
            )
        except AssessmentApplicationError as error:
            raise ExperimentApplicationError(error.status_code, error.detail) from error

    async def freeze_experiment_plan(
        self,
        *,
        db: AsyncSession,
        authoring_store: ExperimentAuthoringStore,
        experiment_id: str,
        actor: Actor,
        accepted_version_id: str | None = None,
    ) -> Experiment:
        """Freeze the experiment's plan — the teacher's approval.

        Identical to production (teacher-gated, ownership enforced). Freezing now
        ONLY accepts the plan; generating the exit assessment (``create_assessment``)
        and the class revision note (``create_review_note`` → H1) are separate,
        explicit teacher steps, so the lesson-prep workflow reads as deliberate
        steps rather than a single hidden cascade.

        ``accepted_version_id`` lets the teacher accept a *revised* head version:
        if they ran the feedback loop, each turn mints a new ``PlanVersion`` under
        the same plan, but ``experiment.plan_version_id`` still points at the
        version bound when they first authored. Passing the head version_id here
        re-binds the experiment to it (after verifying it belongs to the same
        plan) so the revisions aren't silently discarded at freeze time.
        """
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if experiment.plan_version_id is None:
            raise ExperimentApplicationError(409, "experiment_plan_not_authored")

        if accepted_version_id and accepted_version_id != experiment.plan_version_id:
            experiment = await self._rebind_to_revised_version(
                authoring_store=authoring_store,
                experiment=experiment,
                accepted_version_id=accepted_version_id,
            )
        # Re-narrow after the possible rebind reassignment (the rebind always
        # advances to a non-None head version, but the attribute type is widened
        # again by the reassignment).
        plan_version_id = experiment.plan_version_id
        if plan_version_id is None:
            raise ExperimentApplicationError(409, "experiment_plan_not_authored")

        from app.domains.artefacts.types.lesson_plan.deps import (
            lesson_plan_service,
        )

        plan_version = await self.repository.get_plan_version(plan_version_id)
        if plan_version is None:
            raise ExperimentApplicationError(404, "plan_version_not_found")
        if plan_version.status != PlanVersionStatus.APPROVED:
            plan_service = lesson_plan_service(db)
            role_label = "teacher" if actor.role == ROLE_TEACHER else "research manager"
            owner_teacher_id = actor.teacher_id if actor.role == ROLE_TEACHER else None
            await plan_service.approve(
                version_id=plan_version_id,
                approved_by=f"{actor.display_name} ({role_label})",
                owner_teacher_id=owner_teacher_id,
                # The exit assessment + the class revision note are now explicit
                # teacher steps (create_assessment / create_review_note). Freezing
                # only accepts the plan; it fires neither automatically.
                auto_generate_diagnostic=False,
            )
        return experiment

    async def _rebind_to_revised_version(
        self,
        *,
        authoring_store: ExperimentAuthoringStore,
        experiment: Experiment,
        accepted_version_id: str,
    ) -> Experiment:
        """Point the experiment at a revised head version of its own plan.

        Guards against binding an unrelated plan: the accepted version must share
        the ``plan_id`` of the currently-bound version. Returns the experiment with
        ``plan_version_id`` advanced to the accepted head.
        """
        if experiment.plan_version_id is None:
            raise ExperimentApplicationError(409, "experiment_plan_not_authored")
        bound = await self.repository.get_plan_version_plan(
            plan_version_id=experiment.plan_version_id
        )
        if bound is None:
            raise ExperimentApplicationError(409, "accepted_version_belongs_to_other_plan")
        await bind_experiment_plan_version(
            authoring_store,
            experiment_id=experiment.experiment_id,
            plan_version_id=accepted_version_id,
            expected_plan_id=bound[1].plan_id,
            target_not_found_detail="accepted_version_not_found",
        )
        return await self.get_experiment(experiment_id=experiment.experiment_id)

    def _ensure_lesson_matches_workspace(
        self, *, workspace: TeacherWorkspace, lesson_period: LessonPeriod
    ) -> None:
        """The lesson must sit in the workspace's class + subject + term."""
        scheme = lesson_period.scheme_of_work
        if (
            scheme is None
            or workspace.term_class_subject is None
            or scheme.term_class_subject_id != workspace.term_class_subject.id
        ):
            raise ExperimentApplicationError(409, "lesson_period_workspace_mismatch")

    async def create_review_note(
        self,
        *,
        db: AsyncSession,
        experiment_id: str,
        actor: Actor,
        launch: ReviewNoteLauncher,
    ) -> Experiment:
        """Teacher action: generate the class revision note for an accepted lesson.

        Runs the H1 build (the research conditions + the class revision note the
        teacher reviews) in the background. Requires the plan to be authored +
        accepted, and its lesson note approved, first; the owning teacher (or a
        research manager) may trigger it. The execution guard rejects a duplicate
        in-flight/succeeded run, so re-clicking is safe. Errors surface to the caller,
        because this is a deliberate button.
        """
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        plan_version_id = experiment.plan_version_id
        if plan_version_id is None:
            raise ExperimentApplicationError(409, "experiment_plan_not_authored")
        plan_version = await self.repository.get_plan_version(plan_version_id)
        if plan_version is None:
            raise ExperimentApplicationError(404, "plan_version_not_found")
        if plan_version.status != PlanVersionStatus.APPROVED:
            raise ExperimentApplicationError(409, "accept_the_plan_first")
        # The note-reading conditions are grounded in the teacher's lesson note, as the
        # study's were, so the class note waits until the teacher has approved one.
        if await self.repository.approved_lesson_note(plan_version_id) is None:
            raise ExperimentApplicationError(409, "approve_the_lesson_note_first")
        if actor.role == ROLE_TEACHER and actor.teacher_id is not None:
            from app.domains.artefacts.types.lesson_plan.application.ownership import (
                teacher_owns_plan_version,
            )

            owns = await teacher_owns_plan_version(
                db, teacher_id=actor.teacher_id, plan_version_id=plan_version_id
            )
            if not owns:
                raise ExperimentApplicationError(403, "not_your_lesson")

        await launch(
            LaunchExecutionInput(
                experiment_id=experiment.experiment_id,
                hypothesis=Hypothesis.H1,
                runtime_snapshot={"trigger": "teacher_create_review_note"},
                requested_by=actor.auth_id,
            )
        )
        return experiment

    async def list_experiments(
        self,
        *,
        filters: ExperimentListFilters,
    ) -> list[Experiment]:
        experiments = await self.repository.list_experiments(filters=filters)
        if filters.school_id is None:
            return list(experiments)

        matching: list[Experiment] = []
        for experiment in experiments:
            workspace = await self.repository.get_workspace(experiment.teacher_workspace_id)
            school = (
                workspace.term_class_subject.classroom.school
                if workspace
                and workspace.term_class_subject
                and workspace.term_class_subject.classroom
                else None
            )
            if school is not None and school.id == filters.school_id:
                matching.append(experiment)
        return matching

    async def get_experiment(
        self,
        *,
        experiment_id: str,
    ) -> Experiment:
        experiment = await self.repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        return experiment
