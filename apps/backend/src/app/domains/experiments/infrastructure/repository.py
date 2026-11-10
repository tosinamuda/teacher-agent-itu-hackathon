from __future__ import annotations

import uuid
from collections import defaultdict
from collections.abc import Sequence
from typing import cast

from sqlalchemy import and_, case, delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    ApprovedLessonNote,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_notes import (
    SqlAlchemyApprovedLessonNotes,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
)
from app.domains.experiments.application.evaluation_scope import (
    EvaluationBundleScope,
    EvaluationExperimentScope,
    EvaluationFocalCaseScope,
)
from app.domains.experiments.application.filters import ExperimentListFilters
from app.domains.experiments.application.lesson_notes import LessonNoteState
from app.domains.experiments.domain.records import (
    ExperimentAdministrationRecord,
    ExperimentPlanBindingRecord,
)
from app.domains.experiments.domain.types import (
    ExecutionErrorCategory,
    ExecutionStatus,
    Hypothesis,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
    Investigation,
)
from app.domains.learners.models import LearnerProfile
from app.domains.school.models.structure import Class, Course
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace
from app.shared.time import utc_now


class ExperimentRepository:
    """Queries over experiments; the caller owns the transaction.

    Bound to one session for its whole life — there is no per-call session
    argument. Whoever opened that session decides when it commits.
    """

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def evaluation_scope(self, *, experiment_id: str) -> EvaluationExperimentScope | None:
        result = await self._db.execute(
            select(Experiment).where(Experiment.experiment_id == experiment_id)
        )
        experiment = result.scalars().first()
        if experiment is None:
            return None
        return EvaluationExperimentScope(
            id=experiment.id,
            experiment_id=experiment.experiment_id,
            lesson_period_id=experiment.lesson_period_id,
        )

    async def evaluation_scope_for_execution(
        self, *, execution_id: uuid.UUID
    ) -> EvaluationExperimentScope | None:
        result = await self._db.execute(
            select(Experiment)
            .join(ExperimentExecution, ExperimentExecution.experiment_db_id == Experiment.id)
            .where(ExperimentExecution.id == execution_id)
        )
        experiment = result.scalars().first()
        if experiment is None:
            return None
        return EvaluationExperimentScope(
            id=experiment.id,
            experiment_id=experiment.experiment_id,
            lesson_period_id=experiment.lesson_period_id,
        )

    async def lock_evaluation_scope(self, *, experiment_db_id: uuid.UUID) -> None:
        await self._db.execute(
            select(Experiment.id).where(Experiment.id == experiment_db_id).with_for_update()
        )

    async def lesson_period_exists(self, *, lesson_period_id: uuid.UUID) -> bool:
        result = await self._db.execute(
            select(LessonPeriod.id).where(LessonPeriod.id == lesson_period_id)
        )
        return result.scalar_one_or_none() is not None

    async def lesson_period_title(self, *, lesson_period_id: uuid.UUID) -> str | None:
        result = await self._db.execute(
            select(LessonPeriod.title).where(LessonPeriod.id == lesson_period_id)
        )
        return result.scalar_one_or_none()

    async def focal_case_belongs_to_experiment(
        self,
        *,
        experiment_db_id: uuid.UUID,
        focal_case_id: str,
    ) -> bool:
        result = await self._db.execute(
            select(ExperimentFocalCase.id)
            .join(
                ExperimentExecution,
                ExperimentExecution.id == ExperimentFocalCase.execution_db_id,
            )
            .where(
                ExperimentFocalCase.experiment_focal_case_id == focal_case_id,
                ExperimentExecution.experiment_db_id == experiment_db_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def evaluation_bundle_scope(self, *, experiment_id: str) -> EvaluationBundleScope | None:
        experiment = await self.evaluation_scope(experiment_id=experiment_id)
        if experiment is None:
            return None
        execution_ids = tuple(
            (
                await self._db.execute(
                    select(ExperimentExecution.id).where(
                        ExperimentExecution.experiment_db_id == experiment.id
                    )
                )
            )
            .scalars()
            .all()
        )
        if not execution_ids:
            focal_cases: tuple[EvaluationFocalCaseScope, ...] = ()
        else:
            rows = (
                await self._db.execute(
                    select(
                        ExperimentFocalCase.experiment_focal_case_id,
                        ExperimentFocalCase.student_id,
                        ExperimentFocalCase.focal_case_type,
                    ).where(ExperimentFocalCase.execution_db_id.in_(execution_ids))
                )
            ).all()
            focal_cases = tuple(
                EvaluationFocalCaseScope(
                    focal_case_id=row.experiment_focal_case_id,
                    student_id=row.student_id,
                    focal_case_type=row.focal_case_type,
                )
                for row in rows
            )
        return EvaluationBundleScope(
            experiment=experiment,
            execution_ids=execution_ids,
            focal_cases=focal_cases,
        )

    async def get_workspace(
        self,
        workspace_id: uuid.UUID,
    ) -> TeacherWorkspace | None:
        result = await self._db.execute(
            select(TeacherWorkspace)
            .where(TeacherWorkspace.id == workspace_id)
            .options(
                joinedload(TeacherWorkspace.teacher),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.classroom)
                .joinedload(Class.school),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.subject),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.grade_level),
            )
        )
        return result.scalars().first()

    async def list_workspaces_by_ids(
        self,
        workspace_ids: Sequence[uuid.UUID],
    ) -> list[TeacherWorkspace]:
        if not workspace_ids:
            return []
        result = await self._db.execute(
            select(TeacherWorkspace)
            .where(TeacherWorkspace.id.in_(workspace_ids))
            .options(
                joinedload(TeacherWorkspace.teacher),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.classroom)
                .joinedload(Class.school),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.subject),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.grade_level),
            )
        )
        return list(result.scalars().unique().all())

    async def list_researcher_workspaces(
        self,
        *,
        school_id: uuid.UUID | None = None,
    ) -> Sequence[TeacherWorkspace]:
        stmt = (
            select(TeacherWorkspace)
            .join(TeacherWorkspace.term_class_subject)
            .join(TermClassSubject.classroom)
            .join(Class.school)
            .options(
                joinedload(TeacherWorkspace.teacher),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.classroom)
                .joinedload(Class.school),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.subject),
                joinedload(TeacherWorkspace.term_class_subject)
                .joinedload(TermClassSubject.course)
                .joinedload(Course.grade_level),
            )
            .order_by(TeacherWorkspace.created_at.desc())
        )
        if school_id is not None:
            stmt = stmt.where(Class.school_id == school_id)
        result = await self._db.execute(stmt)
        return result.scalars().unique().all()

    async def list_lessons_for_term_class_subject(
        self,
        *,
        term_class_subject_id: uuid.UUID,
    ) -> list[LessonPeriod]:
        result = await self._db.execute(
            select(LessonPeriod)
            .join(LessonPeriod.scheme_of_work)
            .where(SchemeOfWork.term_class_subject_id == term_class_subject_id)
            .options(
                joinedload(LessonPeriod.subtopic),
                joinedload(LessonPeriod.scheme_of_work),
            )
            .order_by(SchemeOfWork.week_number.asc(), LessonPeriod.period_number.asc())
        )
        return list(result.scalars().all())

    async def list_lesson_periods_by_ids(
        self,
        lesson_period_ids: Sequence[uuid.UUID],
    ) -> list[LessonPeriod]:
        if not lesson_period_ids:
            return []
        result = await self._db.execute(
            select(LessonPeriod)
            .where(LessonPeriod.id.in_(lesson_period_ids))
            .options(
                joinedload(LessonPeriod.subtopic),
                joinedload(LessonPeriod.scheme_of_work),
            )
        )
        return list(result.scalars().unique().all())

    async def get_lesson_period(
        self,
        lesson_period_id: uuid.UUID,
    ) -> LessonPeriod | None:
        result = await self._db.execute(
            select(LessonPeriod)
            .where(LessonPeriod.id == lesson_period_id)
            .options(
                joinedload(LessonPeriod.subtopic),
                joinedload(LessonPeriod.scheme_of_work),
            )
        )
        return result.scalars().first()

    async def list_approved_plan_versions_for_session(
        self,
        *,
        lesson_period_id: uuid.UUID,
    ) -> list[tuple[PlanVersion, LessonPlan]]:
        result = await self._db.execute(
            select(PlanVersion, LessonPlan)
            .join(LessonPlan, PlanVersion.plan_id == LessonPlan.plan_id)
            .where(
                LessonPlan.lesson_period_id == lesson_period_id,
                PlanVersion.status == PlanVersionStatus.APPROVED,
            )
            .order_by(
                case((PlanVersion.approved_at.is_(None), 1), else_=0),
                PlanVersion.approved_at.desc(),
                PlanVersion.created_at.desc(),
            )
        )
        return cast(list[tuple[PlanVersion, LessonPlan]], list(result.all()))

    async def list_approved_plan_versions_for_lesson_periods(
        self,
        *,
        lesson_period_ids: Sequence[uuid.UUID],
    ) -> list[tuple[PlanVersion, LessonPlan]]:
        """Batch variant: one ``WHERE lesson_period_id IN (...)`` query.

        Retires the per-lesson loop in ``list_workspace_lessons``. Ordering
        is the same as the single-lesson variant — callers that need
        per-lesson grouping group by ``lesson_plan.lesson_period_id``.
        """
        if not lesson_period_ids:
            return []
        result = await self._db.execute(
            select(PlanVersion, LessonPlan)
            .join(LessonPlan, PlanVersion.plan_id == LessonPlan.plan_id)
            .where(
                LessonPlan.lesson_period_id.in_(lesson_period_ids),
                PlanVersion.status == PlanVersionStatus.APPROVED,
            )
            .order_by(
                case((PlanVersion.approved_at.is_(None), 1), else_=0),
                PlanVersion.approved_at.desc(),
                PlanVersion.created_at.desc(),
            )
        )
        return cast(list[tuple[PlanVersion, LessonPlan]], list(result.all()))

    async def approved_lesson_note(self, plan_version_id: str) -> ApprovedLessonNote | None:
        """The plan version's newest approved lesson note, as the conditions read it."""
        return await SqlAlchemyApprovedLessonNotes().latest(self._db, plan_version_id)

    async def get_plan_version(
        self,
        plan_version_id: str,
    ) -> PlanVersion | None:
        result = await self._db.execute(
            select(PlanVersion).where(PlanVersion.version_id == plan_version_id)
        )
        return result.scalars().first()

    async def get_plan_version_plan(
        self,
        *,
        plan_version_id: str,
    ) -> tuple[PlanVersion, LessonPlan] | None:
        result = await self._db.execute(
            select(PlanVersion, LessonPlan)
            .join(LessonPlan, PlanVersion.plan_id == LessonPlan.plan_id)
            .where(PlanVersion.version_id == plan_version_id)
        )
        row = result.first()
        return cast(tuple[PlanVersion, LessonPlan] | None, row)

    async def list_plan_version_plans_by_ids(
        self,
        plan_version_ids: Sequence[str],
    ) -> list[tuple[PlanVersion, LessonPlan]]:
        if not plan_version_ids:
            return []
        result = await self._db.execute(
            select(PlanVersion, LessonPlan)
            .join(LessonPlan, PlanVersion.plan_id == LessonPlan.plan_id)
            .where(PlanVersion.version_id.in_(plan_version_ids))
        )
        return cast(list[tuple[PlanVersion, LessonPlan]], list(result.all()))

    async def stage_experiment(
        self,
        experiment: ExperimentAdministrationRecord,
    ) -> ExperimentAdministrationRecord:
        self._db.add(experiment)
        return experiment

    async def is_workspace_owned_by_teacher(
        self,
        *,
        workspace_id: uuid.UUID,
        teacher_id: uuid.UUID,
    ) -> bool:
        """Single-row existence check for ``(workspace_id, teacher_id)``.

        Used by ``ExperimentAuthorization`` to gate per-id reads. Returns
        ``True`` iff ``workspace_id`` exists AND is owned by ``teacher_id``.
        """
        result = await self._db.execute(
            select(TeacherWorkspace.id).where(
                TeacherWorkspace.id == workspace_id,
                TeacherWorkspace.teacher_id == teacher_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_experiment(
        self,
        experiment_id: str,
    ) -> Experiment | None:
        result = await self._db.execute(
            select(Experiment).where(Experiment.experiment_id == experiment_id)
        )
        return result.scalars().first()

    async def stage_plan_binding(
        self,
        experiment: ExperimentPlanBindingRecord,
    ) -> ExperimentPlanBindingRecord:
        """Stage an experiment whose plan binding was validated by the command."""
        self._db.add(experiment)
        return experiment

    async def list_experiments(
        self,
        *,
        filters: ExperimentListFilters,
    ) -> Sequence[Experiment]:
        stmt = (
            select(Experiment)
            .join(TeacherWorkspace, Experiment.teacher_workspace_id == TeacherWorkspace.id)
            .order_by(Experiment.created_at.desc())
        )
        if filters.workspace_id is not None:
            stmt = stmt.where(Experiment.teacher_workspace_id == filters.workspace_id)
        if filters.plan_version_id is not None:
            stmt = stmt.where(Experiment.plan_version_id == filters.plan_version_id)
        if filters.teacher_id is not None:
            stmt = stmt.where(TeacherWorkspace.teacher_id == filters.teacher_id)
        if filters.experiment_code is not None:
            stmt = stmt.where(
                Experiment.experiment_code.ilike(f"%{filters.experiment_code.strip()}%")
            )
        if filters.hypothesis is not None or filters.status is not None:
            # LEFT join so experiments with no execution yet (created/eligible) survive.
            stmt = stmt.outerjoin(
                ExperimentExecution,
                ExperimentExecution.experiment_db_id == Experiment.id,
            )
            exec_conditions = []
            if filters.hypothesis is not None:
                exec_conditions.append(ExperimentExecution.hypothesis == filters.hypothesis.value)
            if filters.status is not None:
                exec_conditions.append(ExperimentExecution.status == filters.status)
            match = and_(*exec_conditions)
            if filters.status is None:
                # Lane discovery (hypothesis-only): also keep not-yet-run experiments
                # visible so a researcher can find one and start that hypothesis. An
                # explicit status filter stays strict (no un-run experiments).
                match = or_(match, ExperimentExecution.id.is_(None))
            stmt = stmt.where(match)
        result = await self._db.execute(stmt.limit(filters.limit))
        return result.scalars().unique().all()

    async def evaluation_modes_for_experiments(
        self, experiment_db_ids: Sequence[uuid.UUID]
    ) -> dict[uuid.UUID, str]:
        """Per-experiment evaluation mode derived from its ratings.

        ``synthetic`` (rated only by synthetic raters), ``live`` (only real raters), or
        ``mixed``. Experiments with no ratings are absent from the result. Synthetic
        ratings are flagged ``notes.synthetic == true`` by the synthetic rater.
        """
        if not experiment_db_ids:
            return {}
        # ``as_string()`` reads a JSON scalar (MySQL ``JSON_UNQUOTE(JSON_EXTRACT(...))``).
        # ``max(case(... 1 else 0))`` collapses to 1 if any row matches, else 0.
        synth_marker = EvaluationRating.notes["synthetic"].as_string() == "true"
        live_marker = EvaluationRating.notes["synthetic"].as_string().is_distinct_from("true")
        rows = await self._db.execute(
            select(
                ExperimentExecution.experiment_db_id,
                func.max(case((synth_marker, 1), else_=0)).label("has_synth"),
                func.max(case((live_marker, 1), else_=0)).label("has_live"),
            )
            .select_from(EvaluationRating)
            .join(EvaluationPacket, EvaluationRating.evaluation_packet_db_id == EvaluationPacket.id)
            .join(
                ExperimentExecution,
                EvaluationPacket.execution_db_id == ExperimentExecution.id,
            )
            .where(ExperimentExecution.experiment_db_id.in_(experiment_db_ids))
            .group_by(ExperimentExecution.experiment_db_id)
        )
        modes: dict[uuid.UUID, str] = {}
        for experiment_db_id, has_synth, has_live in rows.all():
            if has_synth and has_live:
                modes[experiment_db_id] = "mixed"
            elif has_synth:
                modes[experiment_db_id] = "synthetic"
            elif has_live:
                modes[experiment_db_id] = "live"
        return modes

    async def get_experiment_by_db_id(
        self,
        experiment_db_id: uuid.UUID,
    ) -> Experiment | None:
        result = await self._db.execute(select(Experiment).where(Experiment.id == experiment_db_id))
        return result.scalars().first()

    async def stage_execution(
        self,
        execution: ExperimentExecution,
    ) -> ExperimentExecution:
        self._db.add(execution)
        await self._db.flush()
        await self._db.refresh(execution)
        return execution

    async def save_focal_case(
        self,
        focal_case: ExperimentFocalCase,
    ) -> ExperimentFocalCase:
        self._db.add(focal_case)
        await self._db.flush()
        await self._db.refresh(focal_case)
        return focal_case

    async def save_packets(
        self,
        *,
        packets: list[EvaluationPacket],
    ) -> list[EvaluationPacket]:
        self._db.add_all(packets)
        await self._db.flush()
        for packet in packets:
            await self._db.refresh(packet)
        return packets

    async def delete_packets(
        self,
        *,
        packet_ids: list[uuid.UUID],
    ) -> None:
        if not packet_ids:
            return
        # Ratings reference packets via FK. A re-export replaces a packet set (e.g.
        # after regeneration, or when a condition leaves the rater queue), so clear
        # the dependent ratings first — they belong to the replaced packet and are
        # stale once it is gone. Without this the delete hits a FK violation.
        await self._db.execute(
            delete(EvaluationRating).where(EvaluationRating.evaluation_packet_db_id.in_(packet_ids))
        )
        result = await self._db.execute(
            select(EvaluationPacket).where(EvaluationPacket.id.in_(packet_ids))
        )
        for packet in result.scalars().all():
            await self._db.delete(packet)
        # Flush, don't commit: the caller (export_packets) re-inserts the new packet
        # set in the SAME transaction, so the replace is atomic — no window where the
        # execution has zero packets, and a failure before the re-insert rolls the
        # delete back too.
        await self._db.flush()

    async def lock_execution_by_public_id(self, execution_id: str) -> None:
        """Row-lock the execution to serialize packet export (``FOR UPDATE``).

        Called as export's FIRST statement on purpose: a locking read does not open
        the REPEATABLE READ snapshot, so the snapshot forms on the NEXT read — after
        we hold the lock and after any rival export has committed. A plain snapshot
        read taken first would miss the rival's packets and double-delete them (the
        same trap fixed in the rater-cap count).
        """
        await self._db.execute(
            select(ExperimentExecution.id)
            .where(ExperimentExecution.execution_id == execution_id)
            .with_for_update()
        )

    async def count_real_ratings_for_packets(self, *, packet_ids: list[uuid.UUID]) -> int:
        """Count ratings on these packets that come from REAL (onboarded) raters.

        Synthetic dry-run raters have ``user_id IS NULL`` and their ratings are
        disposable; real expert ratings (``user_id`` set) must never be silently
        destroyed by a re-export, so export refuses to replace a packet set carrying
        any.
        """
        if not packet_ids:
            return 0
        stmt = (
            select(func.count(EvaluationRating.id))
            .select_from(EvaluationRating)
            .join(EvaluationRater, EvaluationRater.id == EvaluationRating.rater_db_id)
            .where(
                EvaluationRating.evaluation_packet_db_id.in_(packet_ids),
                EvaluationRater.user_id.isnot(None),
            )
        )
        return int((await self._db.execute(stmt)).scalar_one())

    async def mark_execution_running(
        self,
        execution_db_id: uuid.UUID,
        *,
        deliveries: int,
    ) -> None:
        """Record this delivery as the attempt that owns the execution."""
        await self._set_execution(
            execution_db_id,
            status=ExecutionStatus.RUNNING,
            delivery_count=deliveries,
            error_message=None,
            error_category=None,
        )

    async def mark_execution_poisoned(
        self,
        execution_db_id: uuid.UUID,
        *,
        deliveries: int,
        error: str,
    ) -> None:
        """Fail an execution that has been delivered more often than the bound allows."""
        await self._set_execution(
            execution_db_id,
            status=ExecutionStatus.FAILED,
            delivery_count=deliveries,
            error_message=error,
            error_category=ExecutionErrorCategory.POISON.value,
        )

    async def record_terminal_status(
        self,
        execution_db_id: uuid.UUID,
        *,
        status: ExecutionStatus,
        error: str | None,
        error_category: ExecutionErrorCategory | None,
    ) -> None:
        """Write how an attempt ended, leaving its delivery count as claimed."""
        await self._set_execution(
            execution_db_id,
            status=status,
            error_message=error,
            error_category=error_category.value if error_category else None,
        )

    async def _set_execution(
        self,
        execution_db_id: uuid.UUID,
        **values: object,
    ) -> None:
        """Stage one execution-row status write; the caller's store commits it."""
        await self._db.execute(
            update(ExperimentExecution)
            .where(ExperimentExecution.id == execution_db_id)
            .values(updated_at=utc_now(), **values)
        )

    async def get_execution(
        self,
        execution_id: str,
    ) -> ExperimentExecution | None:
        result = await self._db.execute(
            select(ExperimentExecution).where(ExperimentExecution.execution_id == execution_id)
        )
        return result.scalars().first()

    async def get_execution_for_update(
        self,
        execution_id: str,
    ) -> ExperimentExecution | None:
        """Row-lock + return the execution, to serialize status transitions.

        The ops panel (redispatch/cancel) and the worker (claim + terminal write) all
        mutate ``status`` on this row from DIFFERENT processes; taking ``FOR UPDATE``
        first makes those transitions serialize instead of racing to last-writer-wins
        (a cancel clobbered by the worker's SUCCEEDED, a redispatch's clear racing the
        worker's inserts, etc.).
        """
        result = await self._db.execute(
            select(ExperimentExecution)
            .where(ExperimentExecution.execution_id == execution_id)
            .with_for_update()
            # Refresh the in-memory row from the locked read: the worker holds a cached
            # copy from its claim, and the terminal-write guard must see the DB's CURRENT
            # status (a concurrent cancel/redispatch), not the stale cached RUNNING.
            .execution_options(populate_existing=True)
        )
        return result.scalars().first()

    async def clear_execution_generation(
        self,
        execution_db_id: uuid.UUID,
    ) -> None:
        """Delete a prior attempt's partial output so a re-run is idempotent.

        The conditioned runner appends condition runs (+ their artefacts) per attempt, so
        re-dispatching or redelivering without clearing would duplicate them. The caller
        holds the execution ``FOR UPDATE`` lock, so this can't race a concurrent insert.
        Does not commit — composes into the caller's transaction.

        Delete order follows the FK chain (no ``ON DELETE`` cascades): artefacts →
        condition runs → focal cases. An H2 condition run carries ``focal_case_db_id``, so
        the focal cases MUST go last; deleting them first FK-violates (errno 1451).
        """
        run_ids = (
            (
                await self._db.execute(
                    select(ExperimentConditionRun.experiment_condition_run_id).where(
                        ExperimentConditionRun.execution_db_id == execution_db_id
                    )
                )
            )
            .scalars()
            .all()
        )
        if run_ids:
            await self._db.execute(
                delete(Artefact).where(Artefact.experiment_condition_run_id.in_(run_ids))
            )
        await self._db.execute(
            delete(ExperimentConditionRun).where(
                ExperimentConditionRun.execution_db_id == execution_db_id
            )
        )
        await self._db.execute(
            delete(ExperimentFocalCase).where(
                ExperimentFocalCase.execution_db_id == execution_db_id
            )
        )

    async def get_execution_by_db_id(
        self,
        execution_db_id: uuid.UUID,
    ) -> ExperimentExecution | None:
        result = await self._db.execute(
            select(ExperimentExecution).where(ExperimentExecution.id == execution_db_id)
        )
        return result.scalars().first()

    async def list_executions_for_experiment(
        self,
        experiment_db_id: uuid.UUID,
    ) -> list[ExperimentExecution]:
        result = await self._db.execute(
            select(ExperimentExecution)
            .where(ExperimentExecution.experiment_db_id == experiment_db_id)
            .order_by(ExperimentExecution.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_executions_for_experiments(
        self,
        experiment_db_ids: Sequence[uuid.UUID],
    ) -> list[ExperimentExecution]:
        """Batch variant: one ``WHERE experiment_db_id IN (...)`` query."""
        if not experiment_db_ids:
            return []
        result = await self._db.execute(
            select(ExperimentExecution)
            .where(ExperimentExecution.experiment_db_id.in_(experiment_db_ids))
            .order_by(ExperimentExecution.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_condition_runs(
        self,
        execution_db_id: uuid.UUID,
    ) -> list[ExperimentConditionRun]:
        result = await self._db.execute(
            select(ExperimentConditionRun)
            .where(ExperimentConditionRun.execution_db_id == execution_db_id)
            .order_by(ExperimentConditionRun.created_at.asc())
        )
        return list(result.scalars().all())

    async def list_condition_runs_for_executions(
        self,
        execution_db_ids: Sequence[uuid.UUID],
    ) -> list[ExperimentConditionRun]:
        """Batch variant: one ``WHERE execution_db_id IN (...)`` query."""
        if not execution_db_ids:
            return []
        result = await self._db.execute(
            select(ExperimentConditionRun)
            .where(ExperimentConditionRun.execution_db_id.in_(execution_db_ids))
            .order_by(ExperimentConditionRun.created_at.asc())
        )
        return list(result.scalars().all())

    async def list_focal_cases(
        self,
        execution_db_id: uuid.UUID,
    ) -> list[ExperimentFocalCase]:
        result = await self._db.execute(
            select(ExperimentFocalCase)
            .where(ExperimentFocalCase.execution_db_id == execution_db_id)
            .order_by(ExperimentFocalCase.created_at.asc())
        )
        return list(result.scalars().all())

    async def list_student_ids_for_experiment(
        self,
        experiment_public_id: str,
    ) -> set[str]:
        """Public student_ids that participated in any execution of this experiment.

        Union of two sources, since a student can appear as a focal case (H2)
        without yet having a condition run, or as a condition-run subject
        (H1/H2) without being focal. Returns empty set if the experiment, its
        executions, or both participation tables are empty.
        """
        experiment = await self.get_experiment(experiment_public_id)
        if experiment is None:
            return set()
        executions = await self.list_executions_for_experiment(experiment.id)
        execution_db_ids = [execution.id for execution in executions]
        if not execution_db_ids:
            return set()
        focal_result = await self._db.execute(
            select(ExperimentFocalCase.student_id).where(
                ExperimentFocalCase.execution_db_id.in_(execution_db_ids)
            )
        )
        run_result = await self._db.execute(
            select(ExperimentConditionRun.student_id).where(
                ExperimentConditionRun.execution_db_id.in_(execution_db_ids),
                ExperimentConditionRun.student_id.is_not(None),
            )
        )
        return {
            student_id
            for student_id in (
                *focal_result.scalars().all(),
                *run_result.scalars().all(),
            )
            if student_id
        }

    async def list_packets(
        self,
        execution_db_id: uuid.UUID,
    ) -> list[EvaluationPacket]:
        result = await self._db.execute(
            select(EvaluationPacket)
            .where(EvaluationPacket.execution_db_id == execution_db_id)
            .order_by(EvaluationPacket.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_packets_for_executions(
        self,
        execution_db_ids: Sequence[uuid.UUID],
    ) -> list[EvaluationPacket]:
        """Batch variant: one ``WHERE execution_db_id IN (...)`` query."""
        if not execution_db_ids:
            return []
        result = await self._db.execute(
            select(EvaluationPacket)
            .where(EvaluationPacket.execution_db_id.in_(execution_db_ids))
            .order_by(EvaluationPacket.created_at.desc())
        )
        return list(result.scalars().all())

    async def next_attempt_number(
        self,
        *,
        experiment_db_id: uuid.UUID,
        hypothesis: Hypothesis,
    ) -> int:
        result = await self._db.execute(
            select(func.coalesce(func.max(ExperimentExecution.attempt_number), 0)).where(
                ExperimentExecution.experiment_db_id == experiment_db_id,
                ExperimentExecution.hypothesis == hypothesis.value,
            )
        )
        return int(result.scalar() or 0) + 1

    async def next_experiment_code_sequence(
        self,
        *,
        code_prefix: str,
    ) -> int:
        result = await self._db.execute(
            select(Experiment.experiment_code).where(
                Experiment.experiment_code.like(f"{code_prefix}-%")
            )
        )
        sequences = []
        for value in result.scalars().all():
            try:
                sequences.append(int(value.rsplit("-", 1)[-1]))
            except (TypeError, ValueError):
                continue
        return (max(sequences) if sequences else 0) + 1

    async def list_all_learners_for_class(
        self,
        *,
        class_id: uuid.UUID,
    ) -> list[LearnerProfile]:
        result = await self._db.execute(
            select(LearnerProfile)
            .where(LearnerProfile.class_id == class_id)
            .order_by(LearnerProfile.full_name.asc())
        )
        return list(result.scalars().all())

    async def count_learners_for_class(
        self,
        *,
        class_id: uuid.UUID,
    ) -> int:
        result = await self._db.execute(
            select(func.count(LearnerProfile.student_id)).where(LearnerProfile.class_id == class_id)
        )
        return int(result.scalar() or 0)

    async def count_learners_per_class(
        self,
        *,
        class_ids: Sequence[uuid.UUID],
    ) -> dict[uuid.UUID, int]:
        if not class_ids:
            return {}
        result = await self._db.execute(
            select(LearnerProfile.class_id, func.count(LearnerProfile.student_id))
            .where(LearnerProfile.class_id.in_(class_ids))
            .group_by(LearnerProfile.class_id)
        )
        return {row[0]: int(row[1]) for row in result.all()}

    async def count_diagnostics_for_class_plan(
        self,
        *,
        class_id: uuid.UUID,
        plan_version_id: str,
    ) -> int:
        result = await self._db.execute(
            select(func.count(ExitTicketSubmission.id))
            .join(
                LearnerProfile,
                LearnerProfile.student_id == ExitTicketSubmission.student_id,
            )
            .where(
                LearnerProfile.class_id == class_id,
                ExitTicketSubmission.plan_version_id == plan_version_id,
            )
        )
        return int(result.scalar() or 0)

    async def count_diagnostics_per_class_plan(
        self,
        *,
        pairs: Sequence[tuple[uuid.UUID, str]],
    ) -> dict[tuple[uuid.UUID, str], int]:
        """Batch variant: counts grouped by ``(class_id, plan_version_id)``.

        Implementation pre-filters by the union of class_ids and
        plan_version_ids (loose superset that the planner reduces via the
        single-col indexes), groups, then post-filters to the requested
        pairs in Python. Avoids ``(col1, col2) IN (...)`` tuple-IN syntax.
        """
        if not pairs:
            return {}
        class_ids = {pair[0] for pair in pairs}
        plan_version_ids = {pair[1] for pair in pairs}
        result = await self._db.execute(
            select(
                LearnerProfile.class_id,
                ExitTicketSubmission.plan_version_id,
                func.count(ExitTicketSubmission.id),
            )
            .join(
                LearnerProfile,
                LearnerProfile.student_id == ExitTicketSubmission.student_id,
            )
            .where(
                LearnerProfile.class_id.in_(class_ids),
                ExitTicketSubmission.plan_version_id.in_(plan_version_ids),
            )
            .group_by(LearnerProfile.class_id, ExitTicketSubmission.plan_version_id)
        )
        requested = set(pairs)
        return {
            (row[0], row[1]): int(row[2]) for row in result.all() if (row[0], row[1]) in requested
        }

    async def latest_diagnostic_for_learner(
        self,
        *,
        student_id: str,
        plan_version_id: str,
    ) -> ExitTicketSubmission | None:
        result = await self._db.execute(
            select(ExitTicketSubmission)
            .where(
                ExitTicketSubmission.student_id == student_id,
                ExitTicketSubmission.plan_version_id == plan_version_id,
            )
            .order_by(ExitTicketSubmission.created_at.desc())
        )
        return result.scalars().first()

    async def latest_diagnostic_per_student(
        self,
        *,
        student_ids: Sequence[str],
        plan_version_id: str,
    ) -> dict[str, ExitTicketSubmission]:
        """Batch variant: one query returns the LATEST diagnostic per student.

        One ``ORDER BY created_at DESC`` query feeds a newest-first dedupe in
        Python (no ``DISTINCT ON``, which MySQL lacks). Retires the per-learner
        loop in ``list_focal_learner_candidates``. Returns a
        ``{student_id: ExitTicketSubmission}`` map so callers can do a single
        dict lookup per learner.
        """
        if not student_ids:
            return {}
        result = await self._db.execute(
            select(ExitTicketSubmission)
            .where(
                ExitTicketSubmission.student_id.in_(student_ids),
                ExitTicketSubmission.plan_version_id == plan_version_id,
            )
            .order_by(ExitTicketSubmission.created_at.desc())
        )
        latest: dict[str, ExitTicketSubmission] = {}
        for row in result.scalars().all():
            # Rows arrive newest-first, so the first sighting of each student is
            # that student's latest submission.
            latest.setdefault(row.student_id, row)
        return latest

    async def latest_lesson_notes(
        self, plan_version_ids: Sequence[str]
    ) -> dict[str, LessonNoteState]:
        """Each plan version's newest lesson note, and whether it is approved."""
        ids = [plan_version_id for plan_version_id in plan_version_ids if plan_version_id]
        if not ids:
            return {}
        result = await self._db.execute(
            select(Artefact)
            .where(Artefact.artefact_type == ArtefactType.LESSON_NOTE.value)
            .where(Artefact.plan_version_id.in_(ids))
            .order_by(Artefact.created_at.asc(), Artefact.id.asc())
        )
        return {
            artefact.plan_version_id: LessonNoteState(
                artefact_id=artefact.artefact_id,
                approved=artefact.review_status == ArtefactReviewStatus.APPROVED,
            )
            for artefact in result.scalars().all()
        }

    async def current_artefacts_by_condition_run(
        self,
        run_ids: Sequence[str],
    ) -> dict[str, Artefact]:
        """Map each condition-run business id to its CURRENT pack artefact.

        Resolves via the single stored link — ``Artefact.experiment_condition_run_id``
        (an output points back at the run that produced it). 1-or-many-safe: when a
        run owns several artefact versions (e.g. a regenerated C4 pack), the approved
        one wins, else the latest. One query for the whole set (no N+1 over runs).
        """
        ids = [run_id for run_id in run_ids if run_id]
        if not ids:
            return {}
        result = await self._db.execute(
            select(Artefact)
            .where(Artefact.experiment_condition_run_id.in_(ids))
            .order_by(Artefact.created_at.asc())
        )
        by_run: dict[str, list[Artefact]] = defaultdict(list)
        for artefact in result.scalars().all():
            run_id = artefact.experiment_condition_run_id
            if run_id is not None:
                by_run[run_id].append(artefact)
        chosen: dict[str, Artefact] = {}
        for run_id, artefacts in by_run.items():
            approved = [
                a for a in artefacts if a.review_status == ArtefactReviewStatus.APPROVED.value
            ]
            chosen[run_id] = (approved or artefacts)[-1]
        return chosen

    async def current_artefact_for_condition_run(
        self,
        run_id: str,
    ) -> Artefact | None:
        """The single current pack artefact for one condition run (see bulk variant)."""
        return (await self.current_artefacts_by_condition_run([run_id])).get(run_id)

    # --- Investigations (the study: explicit parent of its experiments) ---

    async def stage_investigation(self, investigation: Investigation) -> Investigation:
        self._db.add(investigation)
        return investigation

    async def stage_experiments(self, experiments: Sequence[Experiment]) -> None:
        self._db.add_all(experiments)

    async def get_investigation(self, investigation_id: str) -> Investigation | None:
        result = await self._db.execute(
            select(Investigation).where(Investigation.investigation_id == investigation_id)
        )
        return result.scalars().first()

    async def get_investigation_by_db_id(
        self, investigation_db_id: uuid.UUID
    ) -> Investigation | None:
        result = await self._db.execute(
            select(Investigation).where(Investigation.id == investigation_db_id)
        )
        return result.scalars().first()

    async def list_investigations(self) -> Sequence[Investigation]:
        result = await self._db.execute(
            select(Investigation).order_by(Investigation.created_at.desc())
        )
        return result.scalars().all()

    async def next_investigation_code_sequence(self) -> int:
        result = await self._db.execute(select(Investigation.investigation_code))
        sequences = []
        for value in result.scalars().all():
            try:
                sequences.append(int(value.rsplit("-", 1)[-1]))
            except (TypeError, ValueError):
                continue
        return (max(sequences) if sequences else 0) + 1

    async def list_experiments_for_investigation(
        self, investigation_db_id: uuid.UUID
    ) -> Sequence[Experiment]:
        """Member experiments of a study, oldest first."""
        result = await self._db.execute(
            select(Experiment)
            .where(Experiment.investigation_db_id == investigation_db_id)
            .order_by(Experiment.created_at.asc())
        )
        return result.scalars().all()

    async def count_experiments_for_investigation(
        self, investigation_db_id: uuid.UUID, *, include_sandbox: bool = False
    ) -> int:
        """Count a study's member experiments (real ones only, unless asked)."""
        stmt = select(func.count(Experiment.id)).where(
            Experiment.investigation_db_id == investigation_db_id
        )
        if not include_sandbox:
            stmt = stmt.where(Experiment.is_sandbox.is_(False))
        result = await self._db.execute(stmt)
        return int(result.scalar_one())

    async def list_lesson_period_ids_with_experiments(
        self, *, teacher_workspace_id: uuid.UUID
    ) -> set[uuid.UUID]:
        """Lesson_period ids in this workspace that already have ≥1 experiment."""
        result = await self._db.execute(
            select(Experiment.lesson_period_id)
            .where(Experiment.teacher_workspace_id == teacher_workspace_id)
            .where(Experiment.lesson_period_id.is_not(None))
        )
        return {lesson_period_id for lesson_period_id in result.scalars().all() if lesson_period_id}
