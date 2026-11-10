"""The lesson an experiment runs on, for binding an imported plan to it."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.infrastructure.models import Experiment


async def experiment_lesson(db: AsyncSession, experiment_id: str) -> uuid.UUID | None:
    """The experiment's lesson period, or ``None`` when there is no such experiment."""
    return await db.scalar(
        select(Experiment.lesson_period_id).where(Experiment.experiment_id == experiment_id)
    )
