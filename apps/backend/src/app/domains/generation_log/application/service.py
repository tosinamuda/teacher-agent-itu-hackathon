"""Read side of the generation log: the events of one experiment."""

from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.generation_log.api.schemas import LoggedEvent
from app.domains.generation_log.models.generation_event import GenerationEvent


class GenerationLogService:
    """Queries the generation log for the experiment story."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_for_experiment(
        self,
        *,
        experiment_id: str,
        plan_version_id: str | None = None,
        session_id: str | None = None,
    ) -> list[LoggedEvent]:
        """All recorded events in an experiment's universe (seq ascending).

        An experiment's own condition generations are tagged with ``experiment_id``;
        its diagnostic + base-pack generations carry the shared ``plan_version_id``;
        and the lesson-plan generation is keyed by ``session_id`` (it predates the
        plan version). Matching all three stitches the full pipeline into one story.
        """
        # ``as_string()`` reads a JSON scalar (MySQL ``JSON_UNQUOTE(JSON_EXTRACT(...))``).
        match: list = [GenerationEvent.context["experiment_id"].as_string() == experiment_id]
        if plan_version_id:
            match.append(GenerationEvent.context["plan_version_id"].as_string() == plan_version_id)
        if session_id:
            match.append(GenerationEvent.context["session_id"].as_string() == session_id)
            match.append(GenerationEvent.correlation_id == session_id)
        stmt = select(GenerationEvent).where(or_(*match)).order_by(GenerationEvent.seq.asc())
        rows = (await self._db.execute(stmt)).scalars().all()
        return [LoggedEvent.from_model(row) for row in rows]
