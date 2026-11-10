"""Transactional source-audit item construction and rating submission."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Protocol

from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.evaluation.application import source_audit_builder
from app.domains.evaluation.application.audit_ports import (
    AuditItemBuildStore,
    AuditRatingStore,
)
from app.domains.evaluation.application.constants import _SOURCE_AUDIT_CRITERION_IDS
from app.domains.evaluation.application.errors import EvaluationApplicationError, bounded_int
from app.domains.evaluation.application.peer_ports import (
    PackArtefactsPort,
    TextbookExcerptReader,
)
from app.domains.evaluation.domain.records import AuditItemRecord, AuditRatingRecord
from app.domains.evaluation.domain.types import AuditItemStatus
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView
from app.shared.time import as_utc, utc_now


class AuditRatingConflictError(Exception):
    """A concurrent audit-rating insert won the item/rater unique key."""


class AuditBuildExperiments(Protocol):
    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def lock_execution_by_public_id(
        self, execution_id: str
    ) -> ExperimentExecution | None: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> Sequence[ExperimentConditionRun]: ...


@dataclass(frozen=True)
class AuditBuildDependencies:
    store: AuditItemBuildStore
    experiments: AuditBuildExperiments
    experiment_context: ExperimentContextApplicationService
    artefacts: PackArtefactsPort
    textbook: TextbookExcerptReader


@dataclass(frozen=True)
class AuditBuildResult:
    created: int
    dropped: int
    skipped_executions: int


@dataclass(frozen=True)
class AuditRatingSubmission:
    source_relevance: int
    support_sufficiency: int
    faithfulness: int
    scope_correctness: int
    notes: JsonObject | None


async def build_audit_items(
    dependencies: AuditBuildDependencies,
    *,
    experiment_id: str,
) -> AuditBuildResult:
    experiment = await dependencies.experiments.get_experiment(experiment_id)
    if experiment is None:
        raise EvaluationApplicationError(404, "experiment_not_found")
    context = await dependencies.experiment_context.get_experiment_context(experiment=experiment)
    if context.plan_version is None:
        raise EvaluationApplicationError(409, "experiment_plan_not_authored")
    session_plan = SessionPlanView.model_validate(context.plan_version.session_plan or {})
    executions = await dependencies.experiments.list_executions_for_experiment(experiment.id)
    created = 0
    dropped = 0
    skipped = 0
    for execution in executions:
        try:
            await dependencies.experiments.lock_execution_by_public_id(execution.execution_id)
            existing = await dependencies.store.audit_builds.count_audit_items_for_execution(
                execution_db_id=execution.id
            )
            if existing:
                skipped += 1
                await dependencies.store.commit()
                continue
            items, dropped_here = await _audit_items_for_execution(
                dependencies,
                execution_id=execution.id,
                session_plan=session_plan,
                lesson_id=getattr(context.plan_version, "version_id", None),
            )
            await dependencies.store.audit_builds.stage_audit_items(items)
            await dependencies.store.commit()
            created += len(items)
            dropped += dropped_here
        except Exception:
            await dependencies.store.rollback()
            raise
    return AuditBuildResult(created=created, dropped=dropped, skipped_executions=skipped)


async def _audit_items_for_execution(
    dependencies: AuditBuildDependencies,
    *,
    execution_id: uuid.UUID,
    session_plan: SessionPlanView,
    lesson_id: str | None,
) -> tuple[tuple[AuditItemRecord, ...], int]:
    objective_text_by_id = {
        objective.lesson_objective_id: (objective.objective_text or objective.lesson_objective_id)
        for objective in session_plan.lesson_plan_objectives
        if objective.lesson_objective_id
    }
    scope_boundary = session_plan.subtopic or session_plan.topic
    candidates: list[JsonObject] = []
    figures: dict[str, dict[str, str | None]] = {}
    for run in await dependencies.experiments.list_condition_runs(execution_id):
        if run.condition_code not in source_audit_builder.AUDIT_CONDITIONS:
            continue
        artefact = await dependencies.artefacts.current_artefact_for_condition_run(
            run.experiment_condition_run_id
        )
        if artefact is None:
            continue
        pack = PostClassReviewPack.model_validate(artefact.manifest)
        candidates.extend(
            source_audit_builder.candidate_audit_items(
                condition_code=run.condition_code,
                condition_run_id=run.experiment_condition_run_id,
                lesson_id=lesson_id,
                pack=pack,
                objective_text_by_id=objective_text_by_id,
                scope_boundary=scope_boundary,
            )
        )
        figures.update(source_audit_builder.figures_by_record_id(pack))
    kept, dropped = source_audit_builder.sample_items(candidates)
    references = source_audit_builder.reference_record_map(list(session_plan.references))
    items = [
        await _audit_item_record(
            dependencies.textbook,
            execution_id=execution_id,
            lesson_id=lesson_id,
            candidate=candidate,
            record_id=references.get(str(candidate.get("source_ref") or "")) or None,
            figures=figures,
        )
        for candidate in kept
    ]
    return tuple(items), dropped


async def _audit_item_record(
    textbook: TextbookExcerptReader,
    *,
    execution_id: uuid.UUID,
    lesson_id: str | None,
    candidate: JsonObject,
    record_id: str | None,
    figures: dict[str, dict[str, str | None]],
) -> AuditItemRecord:
    now = utc_now()
    figure = figures.get(record_id) if record_id else None
    return AuditItemRecord(
        id=uuid.uuid4(),
        audit_item_id=new_public_id(PublicIdPrefix.EVALUATION_AUDIT_ITEM),
        execution_db_id=execution_id,
        condition_run_id=str(candidate["condition_run_id"]),
        condition_code=str(candidate["condition_code"]),
        lesson_id=lesson_id,
        lesson_objective_id=_optional_text(candidate.get("lesson_objective_id")),
        objective_text=_optional_text(candidate.get("objective_text")),
        generated_excerpt=str(candidate["generated_excerpt"]),
        source_ref=_optional_text(candidate.get("source_ref")),
        source_record_id=record_id,
        source_excerpt=(
            await textbook.excerpt_for_record(record_id=record_id) if record_id else None
        ),
        figure_url=figure["url"] if figure else None,
        figure_caption=figure["caption"] if figure else None,
        scope_boundary=_optional_text(candidate.get("scope_boundary")),
        status=AuditItemStatus.READY,
        created_at=now,
        updated_at=now,
    )


async def submit_audit_rating(
    store: AuditRatingStore,
    *,
    audit_item_id: str,
    rater_id: str,
    submission: AuditRatingSubmission,
) -> JsonObject:
    persistence = store.audit_ratings
    item = await persistence.audit_item_record(audit_item_id=audit_item_id)
    if item is None:
        raise EvaluationApplicationError(404, "audit_item_not_found")
    rater = await persistence.rater_identity(rater_id=rater_id)
    if rater is None:
        raise EvaluationApplicationError(404, "rater_not_found")
    if not await persistence.audit_item_is_assigned(
        audit_item_id=audit_item_id,
        rater_db_id=rater.id,
    ):
        raise EvaluationApplicationError(403, "rater_not_assigned_to_audit_item")
    values = {
        "source_relevance": submission.source_relevance,
        "support_sufficiency": submission.support_sufficiency,
        "faithfulness": submission.faithfulness,
        "scope_correctness": submission.scope_correctness,
    }
    validated = {
        criterion: bounded_int(
            values[criterion],
            minimum=0,
            maximum=2,
            error_detail=f"audit_{criterion}_out_of_range",
        )
        for criterion in _SOURCE_AUDIT_CRITERION_IDS
    }
    composite = round(sum(validated.values()) / len(validated), 3)
    existing = await persistence.audit_rating_record(
        audit_item_db_id=item.id,
        rater_db_id=rater.id,
    )
    now = utc_now()
    rating = (
        AuditRatingRecord(
            id=uuid.uuid4(),
            rating_id=new_public_id(PublicIdPrefix.EVALUATION_AUDIT_RATING),
            audit_item_db_id=item.id,
            rater_db_id=rater.id,
            source_grounding_score=composite,
            notes=submission.notes,
            created_at=now,
            updated_at=now,
            submitted_at=now,
            **validated,
        )
        if existing is None
        else replace(
            existing,
            source_relevance=validated["source_relevance"],
            support_sufficiency=validated["support_sufficiency"],
            faithfulness=validated["faithfulness"],
            scope_correctness=validated["scope_correctness"],
            source_grounding_score=composite,
            notes=submission.notes,
            updated_at=now,
            submitted_at=now,
        )
    )
    try:
        saved = await persistence.stage_audit_rating(rating)
        await store.commit()
    except AuditRatingConflictError as exc:
        await store.rollback()
        raise EvaluationApplicationError(409, "audit_rating_already_submitted") from exc
    return _audit_rating_payload(saved)


def _audit_rating_payload(rating: AuditRatingRecord) -> JsonObject:
    return {
        "rating_id": rating.rating_id,
        "source_relevance": rating.source_relevance,
        "support_sufficiency": rating.support_sufficiency,
        "faithfulness": rating.faithfulness,
        "scope_correctness": rating.scope_correctness,
        "source_grounding_score": rating.source_grounding_score,
        "submitted_at": as_utc(rating.submitted_at).isoformat() if rating.submitted_at else None,
    }


def _optional_text(value: object) -> str | None:
    return str(value) if value is not None else None
