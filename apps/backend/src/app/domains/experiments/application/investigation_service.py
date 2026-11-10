"""Investigation orchestration: the study is the explicit parent of its experiments.

A study groups experiments under a shared hypothesis. It owns its experiments via
the ``Experiment.investigation_db_id`` FK — it is NOT scoped to one workspace, and
its experiments may span several schools/subjects. A study is created empty (name +
optional description); experiments are added to it afterwards.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol

from pydantic import BaseModel

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.investigation_store import InvestigationStore
from app.domains.experiments.domain.types import ExperimentLifecycleStatus, InvestigationStatus
from app.domains.experiments.infrastructure.models import Experiment, Investigation
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.time import utc_now

if TYPE_CHECKING:
    from app.domains.experiments.application.experiment_views.experiment import ExperimentView


class InvestigationExperimentsResult(BaseModel):
    """The member-experiments rollup returned by the investigation resolver."""

    experiments: list[JsonObject]
    experiment_count: int


class InvestigationQueryReader(Protocol):
    async def get_investigation(self, investigation_id: str) -> Investigation | None: ...

    async def list_investigations(self) -> Sequence[Investigation]: ...

    async def count_experiments_for_investigation(
        self, investigation_db_id: uuid.UUID, *, include_sandbox: bool = False
    ) -> int: ...

    async def list_experiments_for_investigation(
        self, investigation_db_id: uuid.UUID
    ) -> Sequence[Experiment]: ...


class InvestigationExperimentView(Protocol):
    async def __call__(self, *, experiment: Experiment) -> ExperimentView: ...


class InvestigationApplicationService:
    """Read and project studies on top of the experiment machinery."""

    def __init__(
        self,
        repository: InvestigationQueryReader,
    ) -> None:
        self.repository = repository

    async def get_investigation(self, *, investigation_id: str) -> Investigation:
        investigation = await self.repository.get_investigation(investigation_id)
        if investigation is None:
            raise ExperimentApplicationError(404, "investigation_not_found")
        return investigation

    async def list_investigations(self) -> list[tuple[Investigation, int]]:
        investigations = await self.repository.list_investigations()
        out: list[tuple[Investigation, int]] = []
        for investigation in investigations:
            count = await self.repository.count_experiments_for_investigation(investigation.id)
            out.append((investigation, count))
        return out

    async def build_detail(
        self,
        *,
        investigation: Investigation,
        build_view: InvestigationExperimentView,
    ) -> JsonObject:
        """Project each member experiment for the study dashboard."""
        experiments = await self.repository.list_experiments_for_investigation(investigation.id)
        rows: list[JsonObject] = []
        experiment_count = 0
        for experiment in experiments:
            view = await build_view(experiment=experiment)
            response = view.response
            if not response.is_sandbox:
                experiment_count += 1
            lifecycle = response.lifecycle_status
            rows.append(
                {
                    "experiment_id": response.experiment_id,
                    "experiment_code": response.experiment_code,
                    "lesson_period_id": (
                        str(response.lesson_period_id)
                        if response.lesson_period_id is not None
                        else None
                    ),
                    "lesson_title": response.lesson_title,
                    "lesson_subtitle": response.lesson_subtitle,
                    "school_name": response.school_name,
                    "class_name": response.class_name,
                    "subject_name": response.subject_name,
                    "grade_level": response.grade_level,
                    "term": response.term,
                    "plan_version_id": response.plan_version_id,
                    "status": response.status,
                    "lifecycle_status": getattr(lifecycle, "value", str(lifecycle)),
                    "is_sandbox": response.is_sandbox,
                }
            )

        return InvestigationExperimentsResult(
            experiments=rows,
            experiment_count=experiment_count,
        ).model_dump(mode="json")


async def create_investigation(
    store: InvestigationStore[Investigation, Experiment],
    *,
    title: str,
    description: str | None = None,
) -> Investigation:
    """Create one study, retrying a contended sequential code allocation."""
    investigations = store.investigations

    async def build() -> Investigation:
        sequence = await investigations.next_investigation_code_sequence()
        investigation = Investigation(
            investigation_id=new_public_id(PublicIdPrefix.INVESTIGATION),
            investigation_code=f"INV-{sequence:04d}",
            title=title.strip() or f"Investigation {sequence:04d}",
            description=(description.strip() or None) if description else None,
            status=InvestigationStatus.ACTIVE,
            created_at=utc_now(),
        )
        return await investigations.stage_investigation(investigation)

    try:
        return await store.commit_unique_investigation(build)
    except BaseException:
        await store.rollback()
        raise


async def end_investigation(
    store: InvestigationStore[Investigation, Experiment],
    *,
    investigation_id: str,
    ended_by: str | None,
) -> Investigation:
    """Atomically end a study and every active experiment belonging to it."""
    investigations = store.investigations
    try:
        investigation = await investigations.get_investigation(investigation_id)
        if investigation is None:
            raise ExperimentApplicationError(404, "investigation_not_found")
        ended_at = utc_now()
        experiments = await investigations.list_experiments_for_investigation(investigation.id)
        active_experiments = [
            experiment
            for experiment in experiments
            if experiment.lifecycle_status != ExperimentLifecycleStatus.ENDED
        ]
        for experiment in active_experiments:
            experiment.lifecycle_status = ExperimentLifecycleStatus.ENDED
            experiment.ended_at = ended_at
            experiment.ended_by = ended_by
        investigation.status = InvestigationStatus.ENDED
        investigation.ended_at = ended_at
        investigation.ended_by = ended_by
        await investigations.stage_investigation(investigation)
        await investigations.stage_experiments(active_experiments)
        await store.lesson_conclusions.conclude_where_no_experiment_is_active(
            {e.plan_version_id for e in active_experiments if e.plan_version_id}
        )
        await store.commit()
        return investigation
    except BaseException:
        await store.rollback()
        raise
