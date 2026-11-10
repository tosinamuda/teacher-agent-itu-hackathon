"""Session-bound adapter for the artefact reads evaluation requires."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.models import Artefact, ArtefactPlan
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository


class SqlAlchemyPackArtefacts:
    """Bind evaluation's narrow artefact port to the request session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = ArtefactRepository()

    async def get_plan(self, artefact_plan_id: str) -> ArtefactPlan | None:
        return await self._repository.get_plan(self._session, artefact_plan_id)

    async def current_artefact_for_condition_run(self, run_id: str) -> Artefact | None:
        return await self._repository.current_artefact_for_condition_run(self._session, run_id)
