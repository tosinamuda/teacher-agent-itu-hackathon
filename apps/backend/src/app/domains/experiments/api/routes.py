from __future__ import annotations

import uuid
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import CONFIG
from app.db.deps import get_db
from app.domains.assessments.classwork_schemas import (
    ClassworkCoverageResponse,
    ManualClassworkCreateRequest,
)
from app.domains.experiments.api.deps import (
    execution_identity_reader,
    execution_launch_store,
    experiment_access_reader,
    experiment_administration_store,
    experiment_application_queries,
    experiment_authoring_store,
    experiment_execution_view_query,
    experiment_execution_view_reader,
    experiment_list_query,
    experiment_plan_reuse,
    experiment_story_query,
    experiment_view_query,
    experiment_workflow_query,
    experiment_workspace_catalogue_reader,
    launch_execution,
    packet_export_store,
    synthetic_student_context_query,
)
from app.domains.experiments.api.progress_stream import stream_channel_to_websocket
from app.domains.experiments.api.schemas import (
    CurriculumChoiceResponse,
    EvaluationPacketExportResponse,
    ExperimentApprovedVersionResponse,
    ExperimentCreateRequest,
    ExperimentDetailResponse,
    ExperimentEndRequest,
    ExperimentExecutionCreateRequest,
    ExperimentExecutionResponse,
    ExperimentFocalLearnerSelectionResponse,
    ExperimentFocalLearnerUpdateRequest,
    ExperimentLessonOptionResponse,
    ExperimentManualPlanRequest,
    ExperimentPlanFreezeRequest,
    ExperimentPlanReuseRequest,
    ExperimentPlanReuseResponse,
    ExperimentResponse,
    ExperimentSandboxRequest,
    ExperimentStoryResponse,
    ExperimentWorkspaceOptionResponse,
    UnmappedObjectiveResponse,
)
from app.domains.experiments.api.workflow_schemas import WorkflowSnapshotResponse
from app.domains.experiments.application.authorization import (
    ExperimentAccessReader,
    ExperimentAuthorization,
)
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.execution_launch import (
    LaunchExecution,
    LaunchExecutionInput,
    retry_condition,
)
from app.domains.experiments.application.experiment_administration import (
    end_experiment as end_experiment_command,
)
from app.domains.experiments.application.experiment_administration import (
    set_sandbox as set_sandbox_command,
)
from app.domains.experiments.application.experiment_administration import (
    update_focal_learners as update_focal_learners_command,
)
from app.domains.experiments.application.experiment_administration_store import (
    ExperimentAdministrationStore,
)
from app.domains.experiments.application.experiment_authoring_store import (
    ExperimentAuthoringStore,
)
from app.domains.experiments.application.experiment_context_service import (
    ExperimentWorkspaceCatalogueReader,
)
from app.domains.experiments.application.experiment_plan_reuse import (
    ExperimentPlanReuse,
    PlanReuseRequest,
)
from app.domains.experiments.application.experiment_story_service import (
    ExperimentStoryApplicationService,
)
from app.domains.experiments.application.experiment_views import (
    ExperimentExecutionViewQuery,
    ExperimentExecutionViewReader,
    ExperimentListQuery,
    ExperimentViewQuery,
    SyntheticStudentContextQuery,
    execution_payload,
    list_workspace_lesson_approved_versions,
    list_workspace_lesson_options,
    list_workspace_options,
    render_evaluation_packet_response,
)
from app.domains.experiments.application.filters import ExperimentListFilters
from app.domains.experiments.application.launch_ports import ExecutionLaunchStore
from app.domains.experiments.application.lookups import (
    ExecutionIdentityReader,
    execution_or_error,
    experiment_or_error,
)
from app.domains.experiments.application.packet_export_service import (
    PacketExportApplicationService,
)
from app.domains.experiments.application.packet_export_store import PacketExportStore
from app.domains.experiments.application.service import (
    ExperimentApplicationQueries,
    ExperimentApplicationService,
)
from app.domains.experiments.application.synthetic_progress import synthetic_channel
from app.domains.experiments.application.workflow_query import (
    ExperimentWorkflowQuery,
)
from app.domains.experiments.domain.types import Hypothesis
from app.domains.jobs.api.schemas import JobAccepted
from app.infra.jobs.deps import job_queue
from app.infra.jobs.kinds import (
    AUTHOR_EXPERIMENT_PLAN,
    SYNTHETIC_LOOP,
    SYNTHETIC_RATE,
    SYNTHETIC_STUDENTS,
    SYNTHETIC_TEACHER,
)
from app.infra.jobs.queue import JobQueue
from app.shared.auth import (
    ROLE_ADMIN,
    Actor,
    get_actor,
)
from app.shared.authz import requires
from app.shared.json_types import JsonObject

router = APIRouter(prefix="/experiments", tags=["experiments"])


def _raise_http_error(error: ExperimentApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


# ===== Workspace + lesson catalogue =====


@router.get("/workspaces", response_model=list[ExperimentWorkspaceOptionResponse])
async def list_experiment_workspaces(
    school_id: uuid.UUID | None = None,
    repository: ExperimentWorkspaceCatalogueReader = Depends(experiment_workspace_catalogue_reader),
    actor: Actor = Depends(requires(obj="workspace:*", act="read")),
) -> list[ExperimentWorkspaceOptionResponse]:
    """List teacher workspaces eligible for experiment use.

    Researcher (and other wildcard roles) see every workspace; a teacher sees
    only the workspaces they teach. The teacher filter is server-set from the
    actor — callers can't widen it by guessing UUIDs.
    """
    teacher_id_filter = None if actor.is_research_manager else actor.teacher_id
    return await list_workspace_options(
        repository, school_id=school_id, teacher_id=teacher_id_filter
    )


@router.get(
    "/workspaces/{workspace_id}/lessons",
    response_model=list[ExperimentLessonOptionResponse],
)
async def list_workspace_lessons(
    workspace_id: uuid.UUID,
    repository: ExperimentWorkspaceCatalogueReader = Depends(experiment_workspace_catalogue_reader),
    _actor: Actor = Depends(requires(obj="workspace:*", act="read")),
) -> list[ExperimentLessonOptionResponse]:
    """List runnable lessons for a workspace + their under-research flag."""
    try:
        return await list_workspace_lesson_options(repository, workspace_id=workspace_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)


@router.get(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/approved-versions",
    response_model=list[ExperimentApprovedVersionResponse],
)
async def list_workspace_lesson_versions(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    repository: ExperimentWorkspaceCatalogueReader = Depends(experiment_workspace_catalogue_reader),
    _actor: Actor = Depends(requires(obj="workspace:*", act="read")),
) -> list[ExperimentApprovedVersionResponse]:
    """List approved plan versions for a specific workspace + lesson pair."""
    try:
        return await list_workspace_lesson_approved_versions(
            repository, workspace_id=workspace_id, lesson_period_id=lesson_period_id
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)


# ===== Experiment CRUD =====


@router.post("", response_model=ExperimentResponse)
async def create_experiment(
    payload: ExperimentCreateRequest,
    db: AsyncSession = Depends(get_db),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    _actor: Actor = Depends(requires(obj="experiment:*", act="create")),
) -> ExperimentResponse:
    """Create an experiment for one (workspace, lesson) inside a study.

    Researcher-only: this stands up the experiment container under its parent study.
    Multiple experiments per lesson are allowed. The assigned teacher authors +
    freezes its own plan afterwards (see the plan routes below).
    """
    service = ExperimentApplicationService(queries)
    try:
        experiment = await service.create_experiment(
            db=db,
            investigation_id=payload.investigation_id,
            teacher_workspace_id=payload.teacher_workspace_id,
            lesson_period_id=payload.lesson_period_id,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    view = await view_query.build_view(experiment=experiment)
    return view.response


@router.post("/{experiment_id}/plan", response_model=JobAccepted, status_code=202)
async def author_experiment_plan(
    experiment_id: str,
    db: AsyncSession = Depends(get_db),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
) -> JobAccepted:
    """Queue the experiment's OWN plan draft — the assigned teacher's action.

    The draft mints a fresh plan on the experiment's lesson (separate from production) and
    binds it; follow the job it returns. Gated to a teacher who teaches the class (a
    research-manager bypasses), refused at once when it could not be drafted.
    """
    try:
        await ExperimentApplicationService(queries).check_plan_authoring(
            db=db, experiment_id=experiment_id, actor=actor
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    job_id = await JobQueue(db).ensure(
        AUTHOR_EXPERIMENT_PLAN, experiment_id, subject=experiment_id, requested_by=actor.auth_id
    )
    return JobAccepted(job_id=job_id)


@router.post("/{experiment_id}/plan/manual", response_model=ExperimentResponse)
async def author_experiment_plan_manual(
    experiment_id: str,
    payload: ExperimentManualPlanRequest,
    db: AsyncSession = Depends(get_db),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    authoring_store: ExperimentAuthoringStore = Depends(experiment_authoring_store),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
) -> ExperimentResponse:
    """Author the experiment's plan from hand-entered content (FD-01).

    The manual counterpart of ``POST /{experiment_id}/plan``: instead of LLM
    drafting, the teacher/researcher supplies the plan content. Gated to a teacher
    who teaches the class (a research-manager bypasses); 422 on a validation gap.
    """
    service = ExperimentApplicationService(queries)
    try:
        experiment = await service.author_experiment_plan_manual(
            db=db,
            authoring_store=authoring_store,
            experiment_id=experiment_id,
            actor=actor,
            session_plan_content=payload.session_plan,
            original_document_attachment_id=payload.original_document_attachment_id,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    view = await view_query.build_view(experiment=experiment)
    return view.response


@router.post("/{experiment_id}/plan/reuse", response_model=ExperimentPlanReuseResponse)
async def reuse_experiment_plan(
    experiment_id: str,
    payload: ExperimentPlanReuseRequest,
    reuse: ExperimentPlanReuse = Depends(experiment_plan_reuse),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
) -> ExperimentPlanReuseResponse:
    """Reuse a plan that already exists as the experiment's plan.

    The plan is a saved version or content sent with the request. It keeps its content and is
    saved as a draft for the teacher to accept. While a lesson objective has no curriculum
    objective to point at, nothing is saved and the response lists the choices to make.
    """
    try:
        outcome = await reuse(
            PlanReuseRequest(
                experiment_id=experiment_id,
                actor=actor,
                source_plan_version_id=payload.source_plan_version_id,
                session_plan=payload.session_plan,
                curriculum_choices=payload.curriculum_choices,
            )
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    if outcome.experiment_id is None:
        return ExperimentPlanReuseResponse(
            status="needs_curriculum_choice",
            unmapped=[
                UnmappedObjectiveResponse(
                    lesson_objective_id=str(found["lesson_objective_id"]),
                    objective_text=str(found.get("objective_text") or ""),
                )
                for found in outcome.unmapped
            ],
            choices=[
                CurriculumChoiceResponse(
                    curriculum_objective_id=str(found["curriculum_objective_id"]),
                    objective_text=str(found.get("objective_text") or ""),
                )
                for found in outcome.choices
            ],
        )
    experiment = await queries.get_experiment(outcome.experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="experiment_not_found")
    view = await view_query.build_view(experiment=experiment)
    return ExperimentPlanReuseResponse(status="reused", experiment=view.response)


@router.post("/{experiment_id}/plan/freeze", response_model=ExperimentResponse)
async def freeze_experiment_plan(
    experiment_id: str,
    payload: ExperimentPlanFreezeRequest | None = None,
    db: AsyncSession = Depends(get_db),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    authoring_store: ExperimentAuthoringStore = Depends(experiment_authoring_store),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="freeze_plan")),
) -> ExperimentResponse:
    """Freeze the experiment's plan — the teacher's approval, which triggers C0–C3.

    Same gate + ownership as the production lesson-plan approval. An optional
    ``accepted_version_id`` re-binds the experiment to a revised head version
    (from the feedback loop) before approving, so revisions aren't lost.
    """
    service = ExperimentApplicationService(queries)
    try:
        experiment = await service.freeze_experiment_plan(
            db=db,
            authoring_store=authoring_store,
            experiment_id=experiment_id,
            actor=actor,
            accepted_version_id=payload.accepted_version_id if payload else None,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    view = await view_query.build_view(experiment=experiment)
    return view.response


@router.post("/{experiment_id}/review-note", response_model=ExperimentResponse)
async def create_experiment_review_note(
    experiment_id: str,
    db: AsyncSession = Depends(get_db),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    launch: LaunchExecution = Depends(launch_execution),
    actor: Actor = Depends(requires(obj="pack:*", act="create")),
) -> ExperimentResponse:
    """Teacher action: generate the class revision note for an accepted lesson.

    Kicks off the background build (the research conditions + the class review
    note the teacher reviews). Gated to the owning teacher (a research-manager
    bypasses). Idempotent — re-clicking is rejected by the execution guard.
    """
    service = ExperimentApplicationService(queries)
    try:
        experiment = await service.create_review_note(
            db=db,
            experiment_id=experiment_id,
            actor=actor,
            launch=launch,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    view = await view_query.build_view(experiment=experiment)
    return view.response


@router.post("/{experiment_id}/classwork/manual", response_model=ClassworkCoverageResponse)
async def author_experiment_classwork_manual(
    experiment_id: str,
    payload: ManualClassworkCreateRequest,
    db: AsyncSession = Depends(get_db),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
) -> ClassworkCoverageResponse:
    """Enter the experiment lesson's real classwork by hand (FD-02).

    The classwork counterpart of ``POST /{experiment_id}/plan/manual``. Gated to a
    teacher who teaches the class (a research-manager bypasses); returns the
    items-per-objective coverage report so the UI flags objectives with no items.
    """
    service = ExperimentApplicationService(queries)
    try:
        return await service.author_experiment_classwork_manual(
            db=db, experiment_id=experiment_id, actor=actor, items=payload.items
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)


@router.get("", response_model=list[ExperimentResponse])
async def list_experiments(
    school_id: str | None = None,
    teacher_id: str | None = None,
    teacher_workspace_id: str | None = None,
    workspace_id: str | None = None,
    plan_version_id: str | None = None,
    experiment_code: str | None = None,
    query: str | None = None,
    hypothesis: Hypothesis | None = None,
    status: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    query_service: ExperimentListQuery = Depends(experiment_list_query),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
) -> list[ExperimentResponse]:
    """List experiments matching the filters + optional free-text query.

    Researcher (wildcard) sees all and may pass any teacher_id / workspace_id
    filter. A teacher's view is scope-locked: ``teacher_id`` is forced to the
    actor's user id regardless of what the caller passes, so Teacher Jane can
    never see Teacher Bob's experiments via a forged query string.

    Guard is ``lesson_plan:* / author_plan`` (teacher + researcher) rather than
    ``experiment:* / read`` so the teacher can reach their own plan queue
    without reopening the broader experiment-read surface that was removed when
    researcher-only routes were split out.
    """
    workspace_filter = teacher_workspace_id or workspace_id
    # Researcher and admin both see the whole list — researcher because they
    # own the study; admin because their cross-reference filters (e.g.
    # "students in experiment X" on the user-management page) need it.
    # Teachers stay scope-locked to their own teacher_id (defence in depth).
    if actor.is_research_manager or actor.role == ROLE_ADMIN:
        effective_teacher_id = uuid.UUID(teacher_id) if teacher_id else None
    else:
        effective_teacher_id = actor.teacher_id
    filters = ExperimentListFilters(
        school_id=uuid.UUID(school_id) if school_id else None,
        teacher_id=effective_teacher_id,
        workspace_id=uuid.UUID(workspace_filter) if workspace_filter else None,
        plan_version_id=plan_version_id,
        experiment_code=experiment_code,
        hypothesis=hypothesis,
        status=status,
        query=query,
        limit=limit,
    )
    return await query_service.list_experiments(filters=filters)


@router.put(
    "/{experiment_id}/focal-learners",
    response_model=ExperimentFocalLearnerSelectionResponse,
)
async def update_focal_learners(
    experiment_id: str,
    payload: ExperimentFocalLearnerUpdateRequest,
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    store: ExperimentAdministrationStore = Depends(experiment_administration_store),
    _actor: Actor = Depends(requires(obj="experiment:*", act="update_focal_learners")),
) -> ExperimentFocalLearnerSelectionResponse:
    """Update the teacher's H2 focal-learner selection (validated against class roster)."""
    service = ExperimentApplicationService(queries)
    try:
        await update_focal_learners_command(
            store,
            experiment_id=experiment_id,
            learner_ids=payload.learner_ids,
        )
        experiment = await service.get_experiment(experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    view = await view_query.build_view(experiment=experiment)
    return ExperimentFocalLearnerSelectionResponse(
        experiment_id=experiment.experiment_id,
        learner_ids=list(experiment.focal_learner_ids or []),
        candidates=view.selected_focal_learners,
    )


@router.post("/{experiment_id}/end", response_model=ExperimentResponse)
async def end_experiment(
    experiment_id: str,
    payload: ExperimentEndRequest,
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    store: ExperimentAdministrationStore = Depends(experiment_administration_store),
    _actor: Actor = Depends(requires(obj="experiment:*", act="end")),
) -> ExperimentResponse:
    """End a study (research-manager action) so it stops accepting new executions."""
    service = ExperimentApplicationService(queries)
    try:
        await end_experiment_command(store, experiment_id=experiment_id, ended_by=payload.ended_by)
        experiment = await service.get_experiment(experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    view = await view_query.build_view(experiment=experiment)
    return view.response


@router.post("/{experiment_id}/sandbox", response_model=ExperimentResponse)
async def set_experiment_sandbox(
    experiment_id: str,
    payload: ExperimentSandboxRequest,
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    view_query: ExperimentViewQuery = Depends(experiment_view_query),
    store: ExperimentAdministrationStore = Depends(experiment_administration_store),
    _actor: Actor = Depends(requires(obj="experiment:*", act="set_sandbox")),
) -> ExperimentResponse:
    """Mark/unmark an experiment as a throwaway sandbox (never counts as real)."""
    service = ExperimentApplicationService(queries)
    try:
        await set_sandbox_command(store, experiment_id=experiment_id, is_sandbox=payload.is_sandbox)
        experiment = await service.get_experiment(experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    view = await view_query.build_view(experiment=experiment)
    return view.response


# C4 governance is the classroom teacher's base-pack review + approval (the
# study-pack revision loop + the pack-approve action). It is NOT a separate
# decision form recorded here — that surface was retired. base_pack_approved
# is the C4-ready signal; C4GovernanceApplicationService still owns the
# C3->C4 base-pack gate used by execution + the experiment views.


# ===== Research defaults + story =====


@router.get("/research-defaults")
async def get_research_defaults() -> JsonObject:
    """Return the configured default lesson context for the synthetic harness (a 3rd-term subtopic).

    Declared before ``/{experiment_id}`` so the literal path is matched first.
    """
    defaults = CONFIG.research_defaults
    return {
        "grade": defaults.grade,
        "subject": defaults.subject,
        "term": defaults.term,
        "subtopic": defaults.subtopic,
    }


@router.get("/{experiment_id}/story", response_model=ExperimentStoryResponse)
async def get_experiment_story(
    experiment_id: str,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    story_query: ExperimentStoryApplicationService = Depends(experiment_story_query),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> ExperimentStoryResponse:
    """Render the experiment's pipeline as an ordered, log-traceable story (per-step trace)."""
    try:
        await ExperimentAuthorization(access).load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        story = await story_query.build_experiment_story(db=db, experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return ExperimentStoryResponse.model_validate(story)


# ===== Detail + executions =====


@router.get("/{experiment_id}", response_model=ExperimentDetailResponse)
async def get_experiment(
    experiment_id: str,
    actor: Actor = Depends(get_actor),
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    query_service: ExperimentViewQuery = Depends(experiment_view_query),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> ExperimentDetailResponse:
    """Return the full experiment detail view (header + executions + focal candidates + summary).

    Researcher surface: the teacher role holds no ``experiment:*`` verb, so
    teachers are denied role-wide here (their flows ride ``workspace:*`` /
    ``pack:*``); ``load_and_authorize_experiment`` adds row-level isolation
    for roles that do pass the gate.
    """
    try:
        experiment = await ExperimentAuthorization(access).load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        return await query_service.build_detail(experiment=experiment)
    except ExperimentApplicationError as error:
        _raise_http_error(error)


@router.get("/{experiment_id}/summary", response_model=ExperimentResponse)
async def get_experiment_summary(
    experiment_id: str,
    actor: Actor = Depends(get_actor),
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    query_service: ExperimentViewQuery = Depends(experiment_view_query),
    _actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
) -> ExperimentResponse:
    """Return just the experiment header — the teacher's lesson-prep view.

    The teacher-accessible counterpart to ``get_experiment``: same per-id
    row-level isolation (``load_and_authorize_experiment``), but guarded by
    ``lesson_plan:* / author_plan`` (teacher + researcher) instead of
    ``experiment:* / read``, and returning ONLY the ``ExperimentResponse``
    header — no executions / focal candidates / result summary, which are the
    researcher surfaces the ``experiment:*`` gate protects. Drives the teacher's
    experiment-plan / lesson-prep page, which reads header fields only. The gate
    mirrors ``list_experiments`` so the teacher can reach a single experiment in
    their own plan queue without reopening the broader experiment-read surface.
    """
    try:
        experiment = await ExperimentAuthorization(access).load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        view = await query_service.build_view(experiment=experiment)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return view.response


@router.get("/{experiment_id}/workflow", response_model=WorkflowSnapshotResponse)
async def get_experiment_workflow(
    experiment_id: str,
    actor: Actor = Depends(get_actor),
    query: ExperimentWorkflowQuery = Depends(experiment_workflow_query),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> WorkflowSnapshotResponse:
    """Return the 7-phase / 18-row workflow snapshot for the Overview.

    This is the CQRS read-model port — the frontend previously derived these
    rows client-side from the detail + statistics payloads. The same
    derivation now lives in ``workflow_query.build_snapshot`` so any other
    consumer (CLI, automation, thesis appendix export) sees the same shape.
    """
    try:
        return await query.compute(actor=actor, experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)


@router.post("/{experiment_id}/executions", response_model=ExperimentExecutionResponse)
async def create_experiment_execution(
    experiment_id: str,
    payload: ExperimentExecutionCreateRequest,
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    launch: LaunchExecution = Depends(launch_execution),
    execution_reader: ExperimentExecutionViewReader = Depends(experiment_execution_view_reader),
    actor: Actor = Depends(requires(obj="execution:*", act="create")),
) -> ExperimentExecutionResponse:
    """Start a new execution for an experiment + return the resolved execution DTO."""
    service = ExperimentApplicationService(queries)
    try:
        experiment = await service.get_experiment(experiment_id=experiment_id)
        execution = await launch(
            LaunchExecutionInput(
                experiment_id=experiment_id,
                hypothesis=payload.hypothesis,
                runtime_snapshot=payload.runtime_snapshot,
                requested_by=actor.auth_id,
            )
        )
        return await execution_payload(
            execution_reader,
            experiment_id=experiment.experiment_id,
            execution=execution,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)


@router.post(
    "/{experiment_id}/conditions/{condition_code}/retry",
    response_model=ExperimentExecutionResponse,
)
async def retry_experiment_condition(
    experiment_id: str,
    condition_code: str,
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    store: ExecutionLaunchStore = Depends(execution_launch_store),
    execution_reader: ExperimentExecutionViewReader = Depends(experiment_execution_view_reader),
    _actor: Actor = Depends(requires(obj="execution:*", act="retry")),
) -> ExperimentExecutionResponse:
    """Retry one FAILED H1 condition (research-admin only).

    Regenerates just that pack; the succeeded (frozen) conditions are untouched.
    """
    service = ExperimentApplicationService(queries)
    try:
        experiment = await service.get_experiment(experiment_id=experiment_id)
        execution = await retry_condition(
            store,
            experiment_id=experiment_id,
            condition_code=condition_code,
        )
        return await execution_payload(
            execution_reader,
            experiment_id=experiment.experiment_id,
            execution=execution,
        )
    except ExperimentApplicationError as error:
        _raise_http_error(error)


# ===== Synthetic-test triggers (research-manager only) =====


@router.post("/{experiment_id}/synthetic-students")
async def trigger_synthetic_students(
    experiment_id: str,
    n: int = Query(default=6, ge=1, le=30),
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    context_query: SyntheticStudentContextQuery = Depends(synthetic_student_context_query),
    jobs: JobQueue = Depends(job_queue),
    _actor: Actor = Depends(requires(obj="synthetic:*", act="trigger")),
) -> JsonObject:
    """Queue N synthetic LLM students to answer this lesson's diagnostic (seeds H2)."""
    try:
        experiment = await experiment_or_error(access, experiment_id)
        plan_version_id, class_id = await context_query.resolve(experiment=experiment)
    except ExperimentApplicationError as error:
        _raise_http_error(error)

    await jobs.submit(SYNTHETIC_STUDENTS, plan_version_id, n, class_id, experiment_id)
    return {"status": "queued", "plan_version_id": plan_version_id, "n": n}


@router.post("/{experiment_id}/synthetic-rate")
async def trigger_synthetic_rate(
    experiment_id: str,
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    jobs: JobQueue = Depends(job_queue),
    _actor: Actor = Depends(requires(obj="synthetic:*", act="trigger")),
) -> JsonObject:
    """Queue synthetic expert-teacher raters to score every packet of this experiment."""
    try:
        await experiment_or_error(access, experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)

    await jobs.submit(SYNTHETIC_RATE, experiment_id)
    return {"status": "queued"}


@router.post("/{experiment_id}/synthetic-teacher")
async def trigger_synthetic_teacher(
    experiment_id: str,
    max_rounds: int = Query(default=2, ge=0, le=5),
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    jobs: JobQueue = Depends(job_queue),
    _actor: Actor = Depends(requires(obj="synthetic:*", act="trigger")),
) -> JsonObject:
    """Queue the synthetic teacher to review/approve every pending pack of this experiment."""
    try:
        await experiment_or_error(access, experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)

    await jobs.submit(SYNTHETIC_TEACHER, experiment_id, max_rounds)
    return {"status": "queued"}


@router.post("/{experiment_id}/synthetic-loop")
async def trigger_synthetic_loop(
    experiment_id: str,
    max_rounds: int = Query(default=2, ge=0, le=5),
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    jobs: JobQueue = Depends(job_queue),
    _actor: Actor = Depends(requires(obj="synthetic:*", act="trigger")),
) -> JsonObject:
    """Queue the full synthetic evaluation loop: teacher-review -> export packets -> rate."""
    try:
        await experiment_or_error(access, experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)

    await jobs.submit(SYNTHETIC_LOOP, experiment_id, max_rounds)
    return {"status": "queued"}


# ===== WebSocket streams =====


@router.websocket("/{experiment_id}/synthetic/ws")
async def synthetic_progress_ws(websocket: WebSocket, experiment_id: str) -> None:
    """Live progress stream for an experiment's synthetic test flows (students + ratings)."""
    await stream_channel_to_websocket(websocket, synthetic_channel(experiment_id))


# ===== Execution detail + packet export =====


@router.get("/executions/{execution_id}", response_model=ExperimentExecutionResponse)
async def get_execution(
    execution_id: str,
    query_service: ExperimentExecutionViewQuery = Depends(experiment_execution_view_query),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> ExperimentExecutionResponse:
    """Return the detail DTO for one execution (runs + focal cases + packets)."""
    try:
        return await query_service.build_detail(execution_id=execution_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)


@router.post(
    "/executions/{execution_id}/packets/export",
    response_model=EvaluationPacketExportResponse,
)
async def export_execution_packets(
    execution_id: str,
    executions: ExecutionIdentityReader = Depends(execution_identity_reader),
    store: PacketExportStore = Depends(packet_export_store),
    _actor: Actor = Depends(requires(obj="execution:*", act="export")),
) -> EvaluationPacketExportResponse:
    """Build (or re-use) the rater packets for one execution."""
    try:
        packets = await PacketExportApplicationService(store).export_packets(
            execution_id=execution_id
        )
        execution = await execution_or_error(executions, execution_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return EvaluationPacketExportResponse(
        execution_id=execution.execution_id,
        hypothesis=Hypothesis(execution.hypothesis),
        packet_count=len(packets),
        packets=[render_evaluation_packet_response(packet) for packet in packets],
    )
