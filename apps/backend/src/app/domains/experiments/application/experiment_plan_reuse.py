"""Bring a lesson plan that already exists into an experiment's lesson."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.application.errors import (
    PlanLookupNotFoundError,
    PlanValidationError,
)
from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owns_lesson_period,
)
from app.domains.artefacts.types.lesson_plan.deps import lesson_plan_service
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_authoring import (
    bind_experiment_plan_version,
)
from app.domains.experiments.application.experiment_authoring_store import (
    ExperimentAuthoringStore,
)
from app.domains.experiments.application.lesson_ownership import assert_actor_owns_lesson
from app.domains.experiments.application.service import ExperimentApplicationQueries
from app.shared.auth import ROLE_TEACHER, Actor
from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class PlanReuseRequest:
    experiment_id: str
    actor: Actor
    #: The plan to reuse: a saved plan version, or the plan's content itself. Exactly one.
    source_plan_version_id: str | None
    session_plan: JsonObject | None
    #: The curriculum objective chosen for each lesson objective, by lesson objective id.
    curriculum_choices: Mapping[str, str]


@dataclass(frozen=True)
class PlanReuseOutcome:
    #: The experiment the reused plan is bound to; ``None`` while objectives need a choice.
    experiment_id: str | None
    #: The lesson objectives that need a curriculum objective chosen.
    unmapped: list[JsonObject]
    #: The curriculum objectives of the lesson, to choose from.
    choices: list[JsonObject]


class ExperimentPlanReuse:
    """Reuse an existing plan as the experiment's own, as a draft the teacher reviews."""

    def __init__(
        self,
        db: AsyncSession,
        queries: ExperimentApplicationQueries,
        store: ExperimentAuthoringStore,
    ) -> None:
        self._db = db
        self._queries = queries
        self._store = store

    async def __call__(self, request: PlanReuseRequest) -> PlanReuseOutcome:
        experiment = await self._queries.get_experiment(request.experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if experiment.lesson_period_id is None:
            raise ExperimentApplicationError(409, "experiment_lesson_missing")
        await assert_actor_owns_lesson(
            self._db, actor=request.actor, lesson_period_id=experiment.lesson_period_id
        )
        source, imported_from = await self._source(request)
        teacher_id = request.actor.teacher_id
        try:
            reused = await lesson_plan_service(self._db).reuse_plan(
                session_id=str(experiment.lesson_period_id),
                source=source,
                chosen=request.curriculum_choices,
                teacher_id=str(teacher_id) if teacher_id else None,
                imported_from=imported_from,
            )
        except PlanValidationError as error:
            raise ExperimentApplicationError(422, str(error.detail)) from None
        if reused.plan is None:
            return PlanReuseOutcome(None, reused.unmapped, reused.choices)
        await bind_experiment_plan_version(
            self._store,
            experiment_id=request.experiment_id,
            plan_version_id=reused.plan.version_id,
        )
        return PlanReuseOutcome(request.experiment_id, [], [])

    async def _source(self, request: PlanReuseRequest) -> tuple[JsonObject, str | None]:
        """The content to reuse, and the plan version it came from when it came from one."""
        if request.session_plan is not None:
            return request.session_plan, None
        try:
            found = await lesson_plan_service(self._db).reusable_source(
                request.source_plan_version_id or ""
            )
        except PlanLookupNotFoundError:
            raise ExperimentApplicationError(404, "source_plan_not_found") from None
        actor = request.actor
        if actor.role == ROLE_TEACHER and actor.teacher_id is not None:
            owns = await teacher_owns_lesson_period(
                self._db, teacher_id=actor.teacher_id, lesson_period_id=found.lesson_period_id
            )
            if not owns:
                raise ExperimentApplicationError(403, "not_your_lesson")
        return found.session_plan, found.version_id
