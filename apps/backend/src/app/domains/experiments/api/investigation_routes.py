"""Investigation routes: the study — explicit parent of its experiments.

Registered BEFORE the experiments router in main.py so `GET /experiments/
investigations` isn't captured by `GET /experiments/{experiment_id}`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from fastapi import APIRouter, Depends, HTTPException

from app.domains.experiments.api.deps import (
    experiment_view_query,
    investigation_query_reader,
    investigation_store,
)
from app.domains.experiments.api.schemas import (
    InvestigationCreateRequest,
    InvestigationDetailResponse,
    InvestigationEndRequest,
    InvestigationExperimentRow,
    InvestigationSummaryResponse,
)
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_views import (
    ExperimentViewQuery,
)
from app.domains.experiments.application.investigation_service import (
    InvestigationApplicationService,
    InvestigationQueryReader,
)
from app.domains.experiments.application.investigation_service import (
    create_investigation as create_investigation_command,
)
from app.domains.experiments.application.investigation_service import (
    end_investigation as end_investigation_command,
)
from app.domains.experiments.application.investigation_store import InvestigationStore
from app.shared.auth import Actor
from app.shared.authz import requires

if TYPE_CHECKING:
    # Used only in type annotations on the route's private DTO converters
    # (``_summary``, ``_detail``). Hoisted under ``TYPE_CHECKING`` to keep
    # ``api ↛ models`` clean — transport code may shape ORM rows into
    # response DTOs but must not depend on the ORM at runtime.
    from app.domains.experiments.infrastructure.models import Investigation
from app.shared.json_types import JsonObject

router = APIRouter(prefix="/experiments/investigations", tags=["investigations"])


def _raise_http_error(error: ExperimentApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


def _summary(investigation: Investigation, experiment_count: int) -> InvestigationSummaryResponse:
    return InvestigationSummaryResponse(
        investigation_id=investigation.investigation_id,
        investigation_code=investigation.investigation_code,
        title=investigation.title,
        description=investigation.description,
        status=investigation.status,
        experiment_count=experiment_count,
        ended_at=investigation.ended_at,
        ended_by=investigation.ended_by,
        created_at=investigation.created_at,
    )


def _int(value: object) -> int:
    return value if isinstance(value, int) else 0


def _detail(investigation: Investigation, detail: JsonObject) -> InvestigationDetailResponse:
    raw_experiments = detail.get("experiments", [])
    experiments = [
        InvestigationExperimentRow.model_validate(row)
        for row in (raw_experiments if isinstance(raw_experiments, list) else [])
    ]
    return InvestigationDetailResponse(
        investigation_id=investigation.investigation_id,
        investigation_code=investigation.investigation_code,
        title=investigation.title,
        description=investigation.description,
        status=investigation.status,
        experiment_count=_int(detail.get("experiment_count", 0)),
        ended_at=investigation.ended_at,
        ended_by=investigation.ended_by,
        created_at=investigation.created_at,
        experiments=experiments,
    )


@router.post("", response_model=InvestigationDetailResponse)
async def create_investigation(
    payload: InvestigationCreateRequest,
    repository: InvestigationQueryReader = Depends(investigation_query_reader),
    views: ExperimentViewQuery = Depends(experiment_view_query),
    store: InvestigationStore = Depends(investigation_store),
    _actor: Actor = Depends(requires(obj="study:*", act="create")),
) -> InvestigationDetailResponse:
    service = InvestigationApplicationService(repository)
    try:
        investigation = await create_investigation_command(
            store,
            title=payload.title,
            description=payload.description,
        )
        detail = await service.build_detail(
            investigation=investigation,
            build_view=views.build_view,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return _detail(investigation, detail)


@router.get("", response_model=list[InvestigationSummaryResponse])
async def list_investigations(
    repository: InvestigationQueryReader = Depends(investigation_query_reader),
    _actor: Actor = Depends(requires(obj="study:*", act="read")),
) -> list[InvestigationSummaryResponse]:
    service = InvestigationApplicationService(repository)
    rows = await service.list_investigations()
    return [_summary(investigation, count) for investigation, count in rows]


@router.get("/{investigation_id}", response_model=InvestigationDetailResponse)
async def get_investigation(
    investigation_id: str,
    repository: InvestigationQueryReader = Depends(investigation_query_reader),
    views: ExperimentViewQuery = Depends(experiment_view_query),
    _actor: Actor = Depends(requires(obj="study:*", act="read")),
) -> InvestigationDetailResponse:
    service = InvestigationApplicationService(repository)
    try:
        investigation = await service.get_investigation(investigation_id=investigation_id)
        detail = await service.build_detail(
            investigation=investigation,
            build_view=views.build_view,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return _detail(investigation, detail)


@router.post("/{investigation_id}/end", response_model=InvestigationDetailResponse)
async def end_investigation(
    investigation_id: str,
    payload: InvestigationEndRequest,
    repository: InvestigationQueryReader = Depends(investigation_query_reader),
    views: ExperimentViewQuery = Depends(experiment_view_query),
    store: InvestigationStore = Depends(investigation_store),
    _actor: Actor = Depends(requires(obj="study:*", act="end")),
) -> InvestigationDetailResponse:
    service = InvestigationApplicationService(repository)
    try:
        investigation = await end_investigation_command(
            store, investigation_id=investigation_id, ended_by=payload.ended_by
        )
        detail = await service.build_detail(
            investigation=investigation,
            build_view=views.build_view,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return _detail(investigation, detail)
