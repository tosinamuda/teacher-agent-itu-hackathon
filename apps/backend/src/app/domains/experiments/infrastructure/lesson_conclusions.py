"""Lesson conclusions written to the plan versions, in the ending command's transaction."""

from __future__ import annotations

from collections.abc import Collection

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.experiments.domain.types import ExperimentLifecycleStatus
from app.domains.experiments.infrastructure.models import Experiment
from app.shared.time import utc_now


class SqlAlchemyLessonConclusions:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def conclude_where_no_experiment_is_active(
        self, plan_version_ids: Collection[str]
    ) -> None:
        if not plan_version_ids:
            return
        # The ending experiments are staged, not flushed; they must count as ended.
        await self._db.flush()
        still_running = set(
            (
                await self._db.execute(
                    select(Experiment.plan_version_id)
                    .where(Experiment.plan_version_id.in_(plan_version_ids))
                    .where(Experiment.lifecycle_status != ExperimentLifecycleStatus.ENDED)
                )
            ).scalars()
        )
        concluding = set(plan_version_ids) - still_running
        if not concluding:
            return
        versions = (
            await self._db.execute(
                select(PlanVersion)
                .where(PlanVersion.version_id.in_(concluding))
                .where(PlanVersion.concluded_at.is_(None))
            )
        ).scalars()
        concluded_at = utc_now()
        for version in versions:
            version.concluded_at = concluded_at
