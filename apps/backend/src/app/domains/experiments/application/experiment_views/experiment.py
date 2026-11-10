"""What the dashboard shows for one experiment, and for a list of them.

The single-experiment and list paths differ only in how the inputs are loaded —
one experiment at a time, or all of them in a constant number of ``IN(...)``
reads — so both end at the same ``experiment_view``.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.evaluation.infrastructure.models import EvaluationPacket
from app.domains.experiments.api.schemas import (
    ExperimentDetailResponse,
    ExperimentFocalLearnerOptionResponse,
    ExperimentResponse,
)
from app.domains.experiments.application.c4_base_pack import current_c4_artefact
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
)
from app.domains.experiments.application.experiment_list_loader import ExperimentListReader
from app.domains.experiments.application.experiment_views.execution import (
    execution_payload,
)
from app.domains.experiments.application.experiment_views.experiment_response import (
    assemble_experiment_response,
    focal_candidate_response,
    matches_experiment_query,
)
from app.domains.experiments.application.experiment_views.readiness import readiness_response
from app.domains.experiments.application.filters import ExperimentListFilters
from app.domains.experiments.application.h2_base_pack import BasePack, first_draw_c3_artefact
from app.domains.experiments.application.lesson_notes import LessonNotesReader
from app.domains.experiments.application.loaded_experiment import LoadedExperiment
from app.domains.experiments.application.results_summary_query import (
    ExperimentResultsSummaryQuery,
)
from app.domains.experiments.application.service import ExperimentApplicationQueries
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
    Investigation,
)
from app.domains.learners.models import LearnerProfile
from app.domains.teaching.models import LessonPeriod, TeacherWorkspace


class ExperimentHeaderReader(Protocol):
    """Context, execution, and C4 rows required for one experiment header."""

    async def get_workspace(self, workspace_id: uuid.UUID) -> TeacherWorkspace | None: ...

    async def count_learners_for_class(self, *, class_id: uuid.UUID) -> int: ...

    async def get_lesson_period(self, lesson_period_id: uuid.UUID) -> LessonPeriod | None: ...

    async def get_plan_version_plan(
        self, *, plan_version_id: str
    ) -> tuple[PlanVersion, LessonPlan] | None: ...

    async def count_diagnostics_for_class_plan(
        self, *, class_id: uuid.UUID, plan_version_id: str
    ) -> int: ...

    async def list_all_learners_for_class(self, *, class_id: uuid.UUID) -> list[LearnerProfile]: ...

    async def latest_diagnostic_per_student(
        self, *, student_ids: Sequence[str], plan_version_id: str
    ) -> dict[str, ExitTicketSubmission]: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> list[ExperimentConditionRun]: ...

    async def current_artefact_for_condition_run(self, run_id: str) -> Artefact | None: ...


class ExperimentDetailReader(Protocol):
    """Execution, result-summary, and annotation rows for experiment detail."""

    async def get_execution(self, execution_id: str) -> ExperimentExecution | None: ...

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> list[ExperimentConditionRun]: ...

    async def list_focal_cases(self, execution_db_id: uuid.UUID) -> list[ExperimentFocalCase]: ...

    async def list_packets(self, execution_db_id: uuid.UUID) -> list[EvaluationPacket]: ...

    async def current_artefacts_by_condition_run(
        self, run_ids: Sequence[str]
    ) -> dict[str, Artefact]: ...

    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def evaluation_modes_for_experiments(
        self, experiment_db_ids: Sequence[uuid.UUID]
    ) -> dict[uuid.UUID, str]: ...

    async def get_investigation_by_db_id(
        self, investigation_db_id: uuid.UUID
    ) -> Investigation | None: ...


class ExperimentEvaluationModeReader(Protocol):
    async def evaluation_modes_for_experiments(
        self, experiment_db_ids: Sequence[uuid.UUID]
    ) -> dict[uuid.UUID, str]: ...


@dataclass(frozen=True)
class ExperimentView:
    """One experiment as the dashboard shows it, with the focal learners it selected.

    The two travel together because readiness is computed from both: an
    experiment is H2-ready only when every focal learner it names resolved.
    """

    response: ExperimentResponse
    selected_focal_learners: list[ExperimentFocalLearnerOptionResponse]


class ExperimentViewQuery:
    """Finished header/detail query service injected at HTTP composition roots."""

    def __init__(
        self,
        headers: ExperimentHeaderReader,
        details: ExperimentDetailReader,
        lesson_notes: LessonNotesReader,
    ) -> None:
        self.headers = headers
        self.details = details
        self.lesson_notes = lesson_notes

    async def build_view(self, *, experiment: Experiment) -> ExperimentView:
        return await build_experiment_view(self.headers, self.lesson_notes, experiment=experiment)

    async def build_detail(self, *, experiment: Experiment) -> ExperimentDetailResponse:
        return await build_experiment_detail_view(
            self.headers,
            self.details,
            self.lesson_notes,
            experiment=experiment,
        )


class ExperimentListQuery:
    """Finished batched dashboard-list query injected by the list route."""

    def __init__(
        self,
        queries: ExperimentApplicationQueries,
        rows: ExperimentListReader,
        evaluation_modes: ExperimentEvaluationModeReader,
        lesson_notes: LessonNotesReader,
    ) -> None:
        self.queries = queries
        self.rows = rows
        self.evaluation_modes = evaluation_modes
        self.lesson_notes = lesson_notes

    async def list_experiments(self, *, filters: ExperimentListFilters) -> list[ExperimentResponse]:
        return await list_experiment_views(
            self.queries,
            self.rows,
            self.evaluation_modes,
            self.lesson_notes,
            filters=filters,
        )


async def build_experiment_view(
    experiments: ExperimentHeaderReader,
    lesson_notes: LessonNotesReader,
    *,
    experiment: Experiment,
) -> ExperimentView:
    """Load one experiment's view inputs and render them."""
    context_service = ExperimentContextApplicationService(experiments)
    context = await context_service.get_experiment_context(experiment=experiment)
    executions = await experiments.list_executions_for_experiment(experiment.id)
    focal_learners = await context_service.list_selected_focal_learner_candidates(
        experiment=experiment
    )
    base_pack = await current_c4_artefact(experiments=experiments, experiment=experiment)
    h2_base_pack = await first_draw_c3_artefact(experiments=experiments, experiment=experiment)
    plan_version_id = experiment.plan_version_id or ""
    notes = await lesson_notes.latest_lesson_notes([plan_version_id])
    return experiment_view(
        LoadedExperiment(
            experiment=experiment,
            context=context,
            executions=executions,
            focal_learners=focal_learners,
            base_pack=base_pack,
            h2_base_pack=h2_base_pack,
            lesson_note=notes.get(plan_version_id),
        )
    )


def _approved(pack: BasePack | None) -> bool:
    return pack is not None and pack.review_status == ArtefactReviewStatus.APPROVED


def experiment_view(loaded: LoadedExperiment) -> ExperimentView:
    """Render one loaded experiment, however its inputs were fetched."""
    base_pack, h2_base, note = loaded.base_pack, loaded.h2_base_pack, loaded.lesson_note
    selected_focal_learners = [
        focal_candidate_response(candidate) for candidate in loaded.focal_learners
    ]
    readiness = readiness_response(
        experiment=loaded.experiment,
        context=loaded.context,
        selected_focal_learners=selected_focal_learners,
        base_pack_artefact_id=None if base_pack is None else base_pack.artefact_id,
        base_pack_approved=_approved(base_pack),
        h2_base_pack_artefact_id=None if h2_base is None else h2_base.artefact_id,
        h2_base_approved=_approved(h2_base),
        lesson_note_artefact_id=None if note is None else note.artefact_id,
        lesson_note_approved=note is not None and note.approved,
    )
    return ExperimentView(
        response=assemble_experiment_response(
            experiment=loaded.experiment,
            context=loaded.context,
            executions=loaded.executions,
            readiness=readiness,
        ),
        selected_focal_learners=selected_focal_learners,
    )


async def build_experiment_detail_view(
    experiments: ExperimentHeaderReader,
    details: ExperimentDetailReader,
    lesson_notes: LessonNotesReader,
    *,
    experiment: Experiment,
) -> ExperimentDetailResponse:
    """Assemble the ``ExperimentDetailResponse`` for the GET ``/{experiment_id}`` handler."""
    context_service = ExperimentContextApplicationService(experiments)
    executions = await details.list_executions_for_experiment(experiment.id)
    execution_payloads = [
        await execution_payload(
            details,
            experiment_id=experiment.experiment_id,
            execution=execution,
        )
        for execution in executions
    ]
    latest_summary = None
    if executions:
        latest_summary = await ExperimentResultsSummaryQuery(details).build_results_summary(
            execution_id=executions[0].execution_id
        )
    view = await build_experiment_view(experiments, lesson_notes, experiment=experiment)
    await _annotate_evaluation_mode(
        details, experiment=experiment, experiment_response=view.response
    )
    await _annotate_investigation_parent(
        details, experiment=experiment, experiment_response=view.response
    )
    focal_learner_candidates = [
        focal_candidate_response(candidate)
        for candidate in await context_service.list_focal_learner_candidates(experiment=experiment)
    ]
    return ExperimentDetailResponse(
        experiment=view.response,
        executions=execution_payloads,
        focal_learner_candidates=focal_learner_candidates,
        selected_focal_learners=view.selected_focal_learners,
        latest_summary=latest_summary,
    )


async def list_experiment_views(
    queries: ExperimentApplicationQueries,
    rows: ExperimentListReader,
    evaluation_modes: ExperimentEvaluationModeReader,
    lesson_notes: LessonNotesReader,
    *,
    filters: ExperimentListFilters,
) -> list[ExperimentResponse]:
    """Render every matching experiment, loading all N sets of view inputs at once.

    Same ``LoadedExperiment`` values and same ``experiment_view`` as the detail
    endpoint — only the loading differs, from ~10 queries per experiment to a
    constant number of ``IN(...)`` reads.
    """
    from app.domains.experiments.application.experiment_list_loader import load_experiment_list
    from app.domains.experiments.application.service import ExperimentApplicationService

    matching = await ExperimentApplicationService(queries).list_experiments(filters=filters)
    modes = await evaluation_modes.evaluation_modes_for_experiments(
        [experiment.id for experiment in matching]
    )
    loaded_experiments = await load_experiment_list(
        repository=rows, lesson_notes=lesson_notes, experiments=matching
    )
    responses: list[ExperimentResponse] = []
    for loaded in loaded_experiments:
        response = experiment_view(loaded).response
        response.evaluation_mode = modes.get(loaded.experiment.id)
        responses.append(response)
    if filters.query is None or not filters.query.strip():
        return responses
    return [response for response in responses if matches_experiment_query(response, filters.query)]


async def _annotate_evaluation_mode(
    experiments: ExperimentDetailReader,
    *,
    experiment: Experiment,
    experiment_response: ExperimentResponse,
) -> None:
    """Look up the evaluation mode for this experiment and attach it to the response."""
    modes = await experiments.evaluation_modes_for_experiments([experiment.id])
    experiment_response.evaluation_mode = modes.get(experiment.id)


async def _annotate_investigation_parent(
    experiments: ExperimentDetailReader,
    *,
    experiment: Experiment,
    experiment_response: ExperimentResponse,
) -> None:
    """Attach the parent study's id + code (every experiment has one)."""
    parent = await experiments.get_investigation_by_db_id(experiment.investigation_db_id)
    if parent is not None:
        experiment_response.investigation_id = parent.investigation_id
        experiment_response.investigation_code = parent.investigation_code
