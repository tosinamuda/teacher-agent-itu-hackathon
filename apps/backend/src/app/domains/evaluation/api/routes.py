from __future__ import annotations

from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from app.config import CONFIG
from app.domains.evaluation.api.deps import (
    assignment_store,
    assignment_view_reader,
    audit_build_dependencies,
    audit_detail_reader,
    audit_export_reader,
    audit_queue_reader,
    audit_rating_store,
    blinding_reader,
    dataset_reader,
    experiment_statistics_dependencies,
    h1_packet_detail_dependencies,
    h2_packet_detail_dependencies,
    investigation_rollup_dependencies,
    my_queue_reader,
    packet_queue_dependencies,
    rater_identity_reader,
    rater_list_reader,
    rater_session_actor,
    rating_command_dependencies,
    rating_import_service,
    ratings_summary_dependencies,
)
from app.domains.evaluation.api.schemas import (
    AssignedRaterResponse,
    AuditAssignmentSlotResponse,
    BlindingKeyRowResponse,
    EvaluationMetaResponse,
    EvaluationPacketQueueItemResponse,
    EvaluationRaterResponse,
    EvaluationRaterSessionRequest,
    EvaluationRatingResponse,
    ExperimentAssignmentsResponse,
    H1AssignmentSlotResponse,
    H1PacketDetailResponse,
    H1PacketRatingSaveRequest,
    H2AssignmentSlotResponse,
    H2PacketDetailResponse,
    H2PacketRatingSaveRequest,
    H2SectionRatingSaveRequest,
    MyQueueLineResponse,
    MyQueueResponse,
    RaterAssignmentAuditRequest,
    RaterAssignmentBundleRequest,
    RaterAssignmentBundleResponse,
    RaterAssignmentH1Request,
    RaterAssignmentH2Request,
    RaterAssignmentResponse,
    RatingImportRequest,
    SourceAuditBuildResponse,
    SourceAuditItemDetailResponse,
    SourceAuditQueueItemResponse,
    SourceAuditRatingResponse,
    SourceAuditRatingSaveRequest,
)
from app.domains.evaluation.application.assignment_commands import (
    assign_audit,
    assign_experiment_bundle,
    assign_h1,
    assign_h2,
)
from app.domains.evaluation.application.assignment_ports import AssignmentStore
from app.domains.evaluation.application.assignment_presenter import AssignedRater
from app.domains.evaluation.application.assignment_queries import (
    AssignmentViewReader,
    MyQueueReader,
    RaterListReader,
    experiment_assignment_view,
    my_assignment_queue,
)
from app.domains.evaluation.application.assignment_queries import (
    list_raters as query_raters,
)
from app.domains.evaluation.application.audit_commands import (
    AuditBuildDependencies,
    AuditRatingSubmission,
    build_audit_items,
    submit_audit_rating,
)
from app.domains.evaluation.application.audit_ports import AuditRatingStore
from app.domains.evaluation.application.audit_queries import (
    AuditDetailReader,
    AuditExportReader,
    AuditQueueReader,
    audit_detail,
    audit_queue,
    export_audit_pack,
)
from app.domains.evaluation.application.blinding_queries import (
    BlindingKeyProjector,
    experiment_blinding_key,
)
from app.domains.evaluation.application.dataset_queries import (
    DatasetProjector,
)
from app.domains.evaluation.application.dataset_queries import (
    export_experiment_dataset as query_experiment_dataset,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.experiment_statistics import (
    ExperimentStatisticsDependencies,
)
from app.domains.evaluation.application.experiment_statistics import (
    experiment_statistics as query_experiment_statistics,
)
from app.domains.evaluation.application.export_schemas import ExperimentDataset
from app.domains.evaluation.application.identity_ports import RaterIdentityReader
from app.domains.evaluation.application.investigation_rollup import (
    InvestigationRollupDependencies,
)
from app.domains.evaluation.application.investigation_rollup import (
    investigation_results_rollup as query_investigation_rollup,
)
from app.domains.evaluation.application.packet_detail_queries import (
    get_h1_packet_detail,
    get_h2_packet_detail,
)
from app.domains.evaluation.application.packet_ports import (
    H1PacketDetailDependencies,
    H2PacketDetailDependencies,
    PacketQueueDependencies,
)
from app.domains.evaluation.application.packet_queue_query import list_packet_queue
from app.domains.evaluation.application.rater_identity import rater_for_actor
from app.domains.evaluation.application.rating_commands import (
    H1RatingSubmission,
    H2CandidateSectionRatings,
    H2RatingSubmission,
    H2SectionRating,
    RatingCommandDependencies,
    submit_h1_rating,
    submit_h2_rating,
)
from app.domains.evaluation.application.rating_import_service import (
    OfflineRatingRow,
    RatingImportApplicationService,
)
from app.domains.evaluation.application.ratings_summary import (
    RatingsSummaryDependencies,
)
from app.domains.evaluation.application.ratings_summary import (
    experiment_ratings_summary as query_ratings_summary,
)
from app.domains.evaluation.application.result_schemas import (
    ExperimentRatingsSummary,
    ExperimentStatistics,
    InvestigationResultsRollup,
    RatingImportResult,
)
from app.domains.evaluation.application.worksheet_queries import (
    generate_h1_worksheet,
    generate_h2_worksheet,
)
from app.domains.evaluation.domain.records import AssignmentRecord
from app.shared.auth import Actor
from app.shared.authz import requires
from app.shared.experiment_enums import Hypothesis

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


def _raise_http_error(error: EvaluationApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


def _h2_section_rating(payload: H2SectionRatingSaveRequest) -> H2SectionRating:
    return H2SectionRating(
        section_id=payload.section_id,
        learner_state_suitability=payload.learner_state_suitability,
        scaffolding_appropriateness=payload.scaffolding_appropriateness,
        challenge_calibration=payload.challenge_calibration,
        misconception_support=payload.misconception_support,
        objective_preservation=payload.objective_preservation,
    )


def _h2_rating_submission(payload: H2PacketRatingSaveRequest) -> H2RatingSubmission:
    return H2RatingSubmission(
        candidate_section_scores=tuple(
            H2CandidateSectionRatings(
                candidate_id=candidate.candidate_id,
                section_scores=tuple(_h2_section_rating(row) for row in candidate.section_scores),
            )
            for candidate in payload.candidate_section_scores or []
        ),
        section_scores=tuple(_h2_section_rating(row) for row in payload.section_scores or []),
        base_section_scores=tuple(
            _h2_section_rating(row) for row in payload.base_section_scores or []
        ),
        notes=payload.notes,
    )


@router.get("/meta", response_model=EvaluationMetaResponse)
async def get_evaluation_meta() -> EvaluationMetaResponse:
    """Public study identity for the rater workspace header (mirrors the print packs)."""
    return EvaluationMetaResponse(
        institution_name=CONFIG.institution_name,
        study_title=CONFIG.study_title,
        textbook_name=CONFIG.textbook_name,
    )


@router.post("/raters/session", response_model=EvaluationRaterResponse)
async def create_rater_session(
    payload: EvaluationRaterSessionRequest,
    identities: RaterIdentityReader = Depends(rater_identity_reader),
    actor: Actor = Depends(rater_session_actor),
) -> EvaluationRaterResponse:
    # Self-identification: a rater binds to their own ``EvaluationRater`` profile.
    # Gated on its OWN ``rater_session:*`` verb (NOT the broad ``auth/user:*,
    # create`` that also guards user / school / learner onboarding) so a rater
    # cannot reach those admin endpoints. Raters, admins, and researchers hold it.
    try:
        rater = await rater_for_actor(identities, actor_user_id=actor.teacher_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    _ = payload.display_name  # retained for wire compatibility; identity comes from the actor
    return EvaluationRaterResponse(
        rater_id=rater.rater_id,
        display_name=rater.display_name,
        created_at=rater.created_at,
        updated_at=rater.updated_at,
    )


@router.get("/raters", response_model=list[EvaluationRaterResponse])
async def list_raters(
    raters: RaterListReader = Depends(rater_list_reader),
    _actor: Actor = Depends(requires(obj="assignment:*", act="read")),
) -> list[EvaluationRaterResponse]:
    """Every rater profile — drives the admin "Assign raters" picker.

    Gated on ``assignment:*, read`` (which a rater also holds for their own
    queue). The data set is small, so we don't paginate; the picker filters
    client-side. A rater hitting this learns its peers' display names, which
    is intentionally public within the study.
    """
    identities = await query_raters(raters)
    return [
        EvaluationRaterResponse(
            rater_id=rater.rater_id,
            display_name=rater.display_name,
            created_at=rater.created_at,
            updated_at=rater.updated_at,
        )
        for rater in identities
    ]


@router.get("/h1/packets", response_model=list[EvaluationPacketQueueItemResponse])
async def list_h1_packets(
    rater_id: str,
    dependencies: PacketQueueDependencies = Depends(packet_queue_dependencies),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> list[EvaluationPacketQueueItemResponse]:
    try:
        payload = await list_packet_queue(
            dependencies,
            hypothesis=Hypothesis.H1,
            rater_id=rater_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return [EvaluationPacketQueueItemResponse.model_validate(item) for item in payload]


@router.get("/h2/packets", response_model=list[EvaluationPacketQueueItemResponse])
async def list_h2_packets(
    rater_id: str,
    dependencies: PacketQueueDependencies = Depends(packet_queue_dependencies),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> list[EvaluationPacketQueueItemResponse]:
    try:
        payload = await list_packet_queue(
            dependencies,
            hypothesis=Hypothesis.H2,
            rater_id=rater_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return [EvaluationPacketQueueItemResponse.model_validate(item) for item in payload]


@router.get("/h1/packets/{evaluation_packet_id}", response_model=H1PacketDetailResponse)
async def get_h1_packet(
    evaluation_packet_id: str,
    rater_id: str,
    dependencies: H1PacketDetailDependencies = Depends(h1_packet_detail_dependencies),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> H1PacketDetailResponse:
    try:
        payload = await get_h1_packet_detail(
            dependencies,
            evaluation_packet_id=evaluation_packet_id,
            rater_id=rater_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return H1PacketDetailResponse.model_validate(payload)


@router.get("/h1/packets/{evaluation_packet_id}/worksheet.pdf")
async def download_h1_packet_worksheet(
    evaluation_packet_id: str,
    rater_id: str,
    dependencies: H1PacketDetailDependencies = Depends(h1_packet_detail_dependencies),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> Response:
    try:
        pdf_bytes, filename = await generate_h1_worksheet(
            dependencies,
            evaluation_packet_id=evaluation_packet_id,
            rater_id=rater_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/h2/packets/{evaluation_packet_id}", response_model=H2PacketDetailResponse)
async def get_h2_packet(
    evaluation_packet_id: str,
    rater_id: str,
    dependencies: H2PacketDetailDependencies = Depends(h2_packet_detail_dependencies),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> H2PacketDetailResponse:
    try:
        payload = await get_h2_packet_detail(
            dependencies,
            evaluation_packet_id=evaluation_packet_id,
            rater_id=rater_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return H2PacketDetailResponse.model_validate(payload)


@router.get("/h2/packets/{evaluation_packet_id}/worksheet.pdf")
async def download_h2_packet_worksheet(
    evaluation_packet_id: str,
    rater_id: str,
    dependencies: H2PacketDetailDependencies = Depends(h2_packet_detail_dependencies),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> Response:
    try:
        pdf_bytes, filename = await generate_h2_worksheet(
            dependencies,
            evaluation_packet_id=evaluation_packet_id,
            rater_id=rater_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.put(
    "/h1/packets/{evaluation_packet_id}/ratings",
    response_model=EvaluationRatingResponse,
)
async def save_h1_rating(
    evaluation_packet_id: str,
    payload: H1PacketRatingSaveRequest,
    dependencies: RatingCommandDependencies = Depends(rating_command_dependencies),
    identities: RaterIdentityReader = Depends(rater_identity_reader),
    actor: Actor = Depends(requires(obj="rating:*", act="create")),
) -> EvaluationRatingResponse:
    """Submit / revise an H1 rating.

    Rater identity is derived from the actor — callers can no longer claim to
    be a different rater via the URL.
    """
    try:
        rater = await rater_for_actor(identities, actor_user_id=actor.teacher_id)
        saved = await submit_h1_rating(
            dependencies=dependencies,
            evaluation_packet_id=evaluation_packet_id,
            rater_id=rater.rater_id,
            submission=H1RatingSubmission(
                rubric_scores=payload.rubric_scores,
                notes=payload.notes,
            ),
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return EvaluationRatingResponse.model_validate(saved)


@router.put(
    "/h2/packets/{evaluation_packet_id}/ratings",
    response_model=EvaluationRatingResponse,
)
async def save_h2_rating(
    evaluation_packet_id: str,
    payload: H2PacketRatingSaveRequest,
    dependencies: RatingCommandDependencies = Depends(rating_command_dependencies),
    identities: RaterIdentityReader = Depends(rater_identity_reader),
    actor: Actor = Depends(requires(obj="rating:*", act="create")),
) -> EvaluationRatingResponse:
    """Submit / revise an H2 rating. Rater identity is derived from the actor."""
    try:
        rater = await rater_for_actor(identities, actor_user_id=actor.teacher_id)
        saved = await submit_h2_rating(
            dependencies=dependencies,
            evaluation_packet_id=evaluation_packet_id,
            rater_id=rater.rater_id,
            submission=_h2_rating_submission(payload),
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return EvaluationRatingResponse.model_validate(saved)


@router.get("/experiments/{experiment_id}/ratings", response_model=ExperimentRatingsSummary)
async def experiment_ratings_summary(
    experiment_id: str,
    dependencies: RatingsSummaryDependencies = Depends(ratings_summary_dependencies),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> ExperimentRatingsSummary:
    """Rater-rating progress for a study (research results dashboard)."""
    try:
        return await query_ratings_summary(dependencies, experiment_id=experiment_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)


@router.get("/experiments/{experiment_id}/statistics", response_model=ExperimentStatistics)
async def experiment_statistics(
    experiment_id: str,
    dependencies: ExperimentStatisticsDependencies = Depends(experiment_statistics_dependencies),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> ExperimentStatistics:
    """H1/H2 hypothesis tests + inter-rater reliability for the results dashboard."""
    try:
        return await query_experiment_statistics(dependencies, experiment_id=experiment_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)


@router.get(
    "/investigations/{investigation_id}/results",
    response_model=InvestigationResultsRollup,
)
async def investigation_results_rollup(
    investigation_id: str,
    dependencies: InvestigationRollupDependencies = Depends(investigation_rollup_dependencies),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> InvestigationResultsRollup:
    """Roll up rater results across all experiments in an investigation's scope."""
    try:
        return await query_investigation_rollup(dependencies, investigation_id=investigation_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)


@router.post("/ratings/import", response_model=RatingImportResult)
async def import_ratings(
    payload: RatingImportRequest,
    service: RatingImportApplicationService = Depends(rating_import_service),
    _actor: Actor = Depends(requires(obj="rating:*", act="import")),
) -> RatingImportResult:
    """Bulk-import offline rater ratings (research-manager action)."""
    rows = [
        OfflineRatingRow(
            packet_code=row.packet_code,
            rater_name=row.rater_name,
            overall_score=row.overall_score,
            rubric_scores=dict(row.rubric_scores),
            notes=row.notes,
        )
        for row in payload.ratings
    ]
    return await service.import_ratings(rows=rows)


@router.get(
    "/experiments/{experiment_id}/blinding-key",
    response_model=list[BlindingKeyRowResponse],
)
async def get_experiment_blinding_key(
    experiment_id: str,
    reader: BlindingKeyProjector = Depends(blinding_reader),
    _actor: Actor = Depends(requires(obj="auth/user:*", act="read")),
) -> list[BlindingKeyRowResponse]:
    """RESEARCHER/ADMIN-ONLY de-anonymisation key for printed offline worksheets.

    Recomputes each assigned rater's deterministic candidate order so the
    researcher can resolve "Candidate A on Dr. X's printout of packet EPK-…" back
    to its condition (C0–C3 / P0–P1) when transcribing offline ratings. Gated on
    ``auth/user:*, read`` — raters never hold it; serving this to a rater would
    unblind the study.
    """
    try:
        rows = await experiment_blinding_key(reader, experiment_id=experiment_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return [
        BlindingKeyRowResponse(
            rater_id=row.rater_id,
            rater_name=row.rater_name,
            hypothesis=row.hypothesis,
            group=row.group,
            packet_code=row.packet_code,
            evaluation_packet_id=row.evaluation_packet_id,
            candidate_label=row.candidate_label,
            condition_code=row.condition_code,
        )
        for row in rows
    ]


@router.get("/experiments/{experiment_id}/export")
async def export_experiment_dataset(
    experiment_id: str,
    reader: DatasetProjector = Depends(dataset_reader),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> ExperimentDataset:
    """Flat H1/H2/source-audit rating rows for analysis (protocol §8 export schemas)."""
    try:
        return await query_experiment_dataset(reader, experiment_id=experiment_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)


# --- Source-grounding audit lane (C2-C4) ---


@router.post("/audit/build", response_model=SourceAuditBuildResponse)
async def build_source_audit(
    experiment_id: str,
    dependencies: AuditBuildDependencies = Depends(audit_build_dependencies),
    _actor: Actor = Depends(requires(obj="audit:*", act="build")),
) -> SourceAuditBuildResponse:
    """Materialise source-grounding audit items for an experiment's C2-C4 runs (idempotent)."""
    try:
        result = await build_audit_items(dependencies, experiment_id=experiment_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return SourceAuditBuildResponse.model_validate(result)


@router.get("/audit/pack.pdf")
async def download_source_audit_pack(
    experiment_id: str,
    audits: AuditExportReader = Depends(audit_export_reader),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> Response:
    """Download the offline source-grounding audit pack PDF for an experiment."""
    try:
        pdf_bytes, filename = await export_audit_pack(audits, experiment_id=experiment_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"content-disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/audit/items", response_model=list[SourceAuditQueueItemResponse])
async def list_audit_items(
    rater_id: str,
    audits: AuditQueueReader = Depends(audit_queue_reader),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> list[SourceAuditQueueItemResponse]:
    items = await audit_queue(audits, rater_id=rater_id)
    return [SourceAuditQueueItemResponse.model_validate(item) for item in items]


@router.get("/audit/items/{audit_item_id}", response_model=SourceAuditItemDetailResponse)
async def get_audit_item(
    audit_item_id: str,
    rater_id: str,
    audits: AuditDetailReader = Depends(audit_detail_reader),
    _actor: Actor = Depends(requires(obj="rating:*", act="read")),
) -> SourceAuditItemDetailResponse:
    try:
        detail = await audit_detail(
            audits,
            audit_item_id=audit_item_id,
            rater_id=rater_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return SourceAuditItemDetailResponse.model_validate(detail)


@router.put(
    "/audit/items/{audit_item_id}/ratings",
    response_model=SourceAuditRatingResponse,
)
async def save_audit_rating(
    audit_item_id: str,
    payload: SourceAuditRatingSaveRequest,
    store: AuditRatingStore = Depends(audit_rating_store),
    identities: RaterIdentityReader = Depends(rater_identity_reader),
    actor: Actor = Depends(requires(obj="rating:*", act="create")),
) -> SourceAuditRatingResponse:
    """Submit / revise a source-audit rating. Rater identity from the actor."""
    try:
        rater = await rater_for_actor(identities, actor_user_id=actor.teacher_id)
        saved = await submit_audit_rating(
            store,
            audit_item_id=audit_item_id,
            rater_id=rater.rater_id,
            submission=AuditRatingSubmission(
                source_relevance=payload.source_relevance,
                support_sufficiency=payload.support_sufficiency,
                faithfulness=payload.faithfulness,
                scope_correctness=payload.scope_correctness,
                notes=payload.notes,
            ),
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return SourceAuditRatingResponse.model_validate(saved)


# --- Rater assignments (Phase H) ---


def _assignment_response(
    assignment: AssignmentRecord, experiment_id: str, rater_id: str
) -> RaterAssignmentResponse:
    """Shape an assignment row + the (resolved) experiment / rater public ids."""
    return RaterAssignmentResponse(
        assignment_id=assignment.assignment_id,
        experiment_id=experiment_id,
        rater_id=rater_id,
        hypothesis=assignment.hypothesis,
        scope_id=assignment.scope_id,
        is_adjudicator=assignment.is_adjudicator,
    )


@router.get(
    "/experiments/{experiment_id}/assignments",
    response_model=ExperimentAssignmentsResponse,
)
async def list_experiment_assignments(
    experiment_id: str,
    assignments: AssignmentViewReader = Depends(assignment_view_reader),
    _actor: Actor = Depends(requires(obj="assignment:*", act="read")),
) -> ExperimentAssignmentsResponse:
    """Every assignment slot for one experiment, grouped H1 / H2 / audit.

    Drives the admin "Assign raters" picker: each slot reports the raters
    already on it plus the protocol capacity, so the UI can render "1 / 3"
    style counters without re-counting on the client.
    """
    try:
        view = await experiment_assignment_view(assignments, experiment_id=experiment_id)
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return ExperimentAssignmentsResponse(
        experiment_id=view.experiment_id,
        h1=(
            H1AssignmentSlotResponse(
                lesson_period_id=view.h1.lesson_period_id,
                lesson_title=view.h1.lesson_title,
                raters=[_assigned_rater(r) for r in view.h1.raters],
                capacity=view.h1.capacity,
            )
            if view.h1 is not None
            else None
        ),
        h2=[
            H2AssignmentSlotResponse(
                focal_case_id=slot.focal_case_id,
                student_id=slot.student_id,
                student_full_name=slot.student_full_name,
                focal_case_type=slot.focal_case_type,
                raters=[_assigned_rater(r) for r in slot.raters],
                capacity=slot.capacity,
            )
            for slot in view.h2
        ],
        audit=[
            AuditAssignmentSlotResponse(
                audit_item_id=slot.audit_item_id,
                raters=[_assigned_rater(r) for r in slot.raters],
                adjudicators=[_assigned_rater(r) for r in slot.adjudicators],
                capacity=slot.capacity,
                adjudicator_capacity=slot.adjudicator_capacity,
            )
            for slot in view.audit
        ],
    )


def _assigned_rater(rater: AssignedRater) -> AssignedRaterResponse:
    """Application dataclass → API response."""
    return AssignedRaterResponse(
        assignment_id=rater.assignment_id,
        rater_id=rater.rater_id,
        display_name=rater.display_name,
        is_adjudicator=rater.is_adjudicator,
    )


@router.post(
    "/experiments/{experiment_id}/assignments/h1",
    response_model=RaterAssignmentResponse,
)
async def assign_rater_h1(
    experiment_id: str,
    payload: RaterAssignmentH1Request,
    store: AssignmentStore = Depends(assignment_store),
    actor: Actor = Depends(requires(obj="assignment:*", act="create")),
) -> RaterAssignmentResponse:
    """Assign one rater to one H1 lesson — atomic for the lesson's C0–C3 packets."""
    try:
        assignment = await assign_h1(
            store,
            experiment_id=experiment_id,
            rater_id=payload.rater_id,
            lesson_period_id=payload.lesson_period_id,
            assigned_by=actor.auth_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return _assignment_response(assignment, experiment_id, payload.rater_id)


@router.post(
    "/experiments/{experiment_id}/assignments/h2",
    response_model=RaterAssignmentResponse,
)
async def assign_rater_h2(
    experiment_id: str,
    payload: RaterAssignmentH2Request,
    store: AssignmentStore = Depends(assignment_store),
    actor: Actor = Depends(requires(obj="assignment:*", act="create")),
) -> RaterAssignmentResponse:
    """Assign one rater to one H2 focal learner — atomic for their P0 + P1."""
    try:
        assignment = await assign_h2(
            store,
            experiment_id=experiment_id,
            rater_id=payload.rater_id,
            focal_case_id=payload.focal_case_id,
            assigned_by=actor.auth_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return _assignment_response(assignment, experiment_id, payload.rater_id)


@router.post(
    "/experiments/{experiment_id}/assignments/bundle",
    response_model=RaterAssignmentBundleResponse,
)
async def assign_rater_bundle(
    experiment_id: str,
    payload: RaterAssignmentBundleRequest,
    store: AssignmentStore = Depends(assignment_store),
    actor: Actor = Depends(requires(obj="assignment:*", act="create")),
) -> RaterAssignmentBundleResponse:
    """Assign one rater to the experiment's whole scope (lesson + every focal case).

    Idempotent per scope; per-scope caps still apply. Run it once per rater —
    three raters gives every candidate its 3 expert ratings (protocol target).
    """
    try:
        counts = await assign_experiment_bundle(
            store,
            experiment_id=experiment_id,
            rater_id=payload.rater_id,
            include_audit=payload.include_audit,
            assigned_by=actor.auth_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    return RaterAssignmentBundleResponse(
        experiment_id=experiment_id,
        rater_id=payload.rater_id,
        h1_assigned=counts.h1,
        h2_assigned=counts.h2,
        audit_assigned=counts.audit,
    )


@router.post(
    "/audit-items/{audit_item_id}/assignments",
    response_model=RaterAssignmentResponse,
)
async def assign_rater_audit(
    audit_item_id: str,
    payload: RaterAssignmentAuditRequest,
    store: AssignmentStore = Depends(assignment_store),
    actor: Actor = Depends(requires(obj="assignment:*", act="create")),
) -> RaterAssignmentResponse:
    """Assign a rater to a source-audit item (or as its adjudicator)."""
    try:
        assignment = await assign_audit(
            store,
            audit_item_id=audit_item_id,
            rater_id=payload.rater_id,
            is_adjudicator=payload.is_adjudicator,
            assigned_by=actor.auth_id,
        )
    except EvaluationApplicationError as error:
        _raise_http_error(error)
    # The experiment id isn't in the URL; service resolves it but we don't need it
    # in the response — the assignment id + scope is enough for clients.
    return RaterAssignmentResponse(
        assignment_id=assignment.assignment_id,
        experiment_id="",
        rater_id=payload.rater_id,
        hypothesis=assignment.hypothesis,
        scope_id=assignment.scope_id,
        is_adjudicator=assignment.is_adjudicator,
    )


@router.get("/my-queue", response_model=MyQueueResponse)
async def my_rater_queue(
    queue_reader: MyQueueReader = Depends(my_queue_reader),
    identities: RaterIdentityReader = Depends(rater_identity_reader),
    actor: Actor = Depends(requires(obj="assignment:*", act="read")),
) -> MyQueueResponse:
    """The actor-rater's assignments grouped by hypothesis (drives their landing).

    Researchers / admins hit this and get an empty queue — they don't rate,
    they assign; the gate accepts them but the actor has no bound rater profile.
    """
    if actor.teacher_id is None:
        raise HTTPException(status_code=401, detail="not_authenticated")
    try:
        rater = await rater_for_actor(identities, actor_user_id=actor.teacher_id)
    except EvaluationApplicationError as error:
        if error.detail != "no_rater_identity_bound_to_this_user":
            _raise_http_error(error)
        return MyQueueResponse(rater_id="", h1=[], h2=[], audit=[])
    queue = await my_assignment_queue(queue_reader, rater=rater)
    return MyQueueResponse(
        rater_id=queue.rater_id,
        h1=[MyQueueLineResponse(**line.__dict__) for line in queue.h1],
        h2=[MyQueueLineResponse(**line.__dict__) for line in queue.h2],
        audit=[MyQueueLineResponse(**line.__dict__) for line in queue.audit],
    )
