"""Named interactive H1 and H2 rating commands."""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Protocol, cast

from app.domains.evaluation.application.assignment_scope import AssignmentScope
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.packet_runtime import PacketRuntime, packet_or_error
from app.domains.evaluation.application.peer_ports import PackArtefactsPort
from app.domains.evaluation.application.rating_ports import (
    RatingSubmissionStore,
    SubmittedRatings,
)
from app.domains.evaluation.application.rating_validation import (
    RatingValidationService,
    mean_score,
)
from app.domains.evaluation.domain.records import RatingRecord
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.shared.experiment_enums import Hypothesis
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject, JsonValue
from app.shared.time import utc_now


class RatingConflictError(Exception):
    """A concurrent rating insert won the packet/rater unique key."""


class RatingExperiments(Protocol):
    """Experiment reads needed by interactive rating commands."""

    async def get_execution_by_db_id(
        self, execution_db_id: uuid.UUID
    ) -> ExperimentExecution | None: ...

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> Sequence[ExperimentConditionRun]: ...

    async def list_focal_cases(
        self, execution_db_id: uuid.UUID
    ) -> Sequence[ExperimentFocalCase]: ...


@dataclass(frozen=True)
class H1RatingSubmission:
    rubric_scores: Mapping[str, int | float]
    notes: JsonObject | None


@dataclass(frozen=True)
class H2SectionRating:
    section_id: str
    learner_state_suitability: int
    scaffolding_appropriateness: int
    challenge_calibration: int
    misconception_support: int | None
    objective_preservation: int


@dataclass(frozen=True)
class H2CandidateSectionRatings:
    candidate_id: str
    section_scores: tuple[H2SectionRating, ...]


@dataclass(frozen=True)
class H2RatingSubmission:
    candidate_section_scores: tuple[H2CandidateSectionRatings, ...]
    section_scores: tuple[H2SectionRating, ...]
    base_section_scores: tuple[H2SectionRating, ...]
    notes: JsonObject | None


@dataclass(frozen=True)
class RatingCommandDependencies:
    store: RatingSubmissionStore
    experiments: RatingExperiments
    experiment_context: ExperimentContextApplicationService
    artefacts: PackArtefactsPort


async def submit_h1_rating(
    *,
    dependencies: RatingCommandDependencies,
    evaluation_packet_id: str,
    rater_id: str,
    submission: H1RatingSubmission,
) -> dict[str, object]:
    return await _submit_rating(
        store=dependencies.store,
        experiments=dependencies.experiments,
        experiment_context=dependencies.experiment_context,
        artefacts=dependencies.artefacts,
        hypothesis=Hypothesis.H1,
        evaluation_packet_id=evaluation_packet_id,
        rater_id=rater_id,
        rubric_scores=submission.rubric_scores,
        section_scores=None,
        base_section_scores=None,
        diagnostic_scores=None,
        notes=submission.notes,
    )


async def submit_h2_rating(
    *,
    dependencies: RatingCommandDependencies,
    evaluation_packet_id: str,
    rater_id: str,
    submission: H2RatingSubmission,
) -> dict[str, object]:
    await _assert_rating_assignment(
        store=dependencies.store,
        experiments=dependencies.experiments,
        experiment_context=dependencies.experiment_context,
        hypothesis=Hypothesis.H2,
        evaluation_packet_id=evaluation_packet_id,
        rater_id=rater_id,
    )
    runtime = PacketRuntime(
        dependencies.store.ratings,
        experiment_repository=dependencies.experiments,
        experiment_context_service=dependencies.experiment_context,
    )
    validation = RatingValidationService(dependencies.artefacts)
    section_scores, base_section_scores = await _h2_save_rows(
        runtime=runtime,
        ratings=dependencies.store.ratings,
        validation=validation,
        evaluation_packet_id=evaluation_packet_id,
        submission=submission,
    )
    return await _submit_rating(
        store=dependencies.store,
        experiments=dependencies.experiments,
        experiment_context=dependencies.experiment_context,
        artefacts=dependencies.artefacts,
        hypothesis=Hypothesis.H2,
        evaluation_packet_id=evaluation_packet_id,
        rater_id=rater_id,
        rubric_scores={},
        section_scores=section_scores,
        base_section_scores=base_section_scores,
        diagnostic_scores={},
        notes=submission.notes,
    )


async def _assert_rating_assignment(
    *,
    store: RatingSubmissionStore,
    experiments: RatingExperiments,
    experiment_context: ExperimentContextApplicationService,
    hypothesis: Hypothesis,
    evaluation_packet_id: str,
    rater_id: str,
) -> None:
    runtime = PacketRuntime(
        store.ratings,
        experiment_repository=experiments,
        experiment_context_service=experiment_context,
    )
    rater = await runtime.rater_or_error(rater_id=rater_id)
    packet = await packet_or_error(store.ratings, evaluation_packet_id=evaluation_packet_id)
    if packet.hypothesis != hypothesis.value:
        raise EvaluationApplicationError(409, "packet_hypothesis_mismatch")
    assignments = AssignmentScope(store.ratings, experiment_repository=experiments)
    if not await assignments.is_packet_assigned(
        packet=packet,
        hypothesis=hypothesis,
        rater_db_id=rater.id,
    ):
        raise EvaluationApplicationError(403, "rater_not_assigned_to_packet")


async def _submit_rating(
    *,
    store: RatingSubmissionStore,
    experiments: RatingExperiments,
    experiment_context: ExperimentContextApplicationService,
    artefacts: PackArtefactsPort,
    hypothesis: Hypothesis,
    evaluation_packet_id: str,
    rater_id: str,
    rubric_scores: Mapping[str, int | float],
    section_scores: list[dict[str, object]] | None,
    base_section_scores: list[dict[str, object]] | None,
    diagnostic_scores: JsonObject | None,
    notes: JsonObject | None,
) -> dict[str, object]:
    persistence = store.ratings
    runtime = PacketRuntime(
        persistence,
        experiment_repository=experiments,
        experiment_context_service=experiment_context,
    )
    validation = RatingValidationService(artefacts)
    assignments = AssignmentScope(persistence, experiment_repository=experiments)
    rater = await runtime.rater_or_error(rater_id=rater_id)
    packet = await packet_or_error(persistence, evaluation_packet_id=evaluation_packet_id)
    if packet.hypothesis != hypothesis.value:
        raise EvaluationApplicationError(409, "packet_hypothesis_mismatch")
    if not await assignments.is_packet_assigned(
        packet=packet,
        hypothesis=hypothesis,
        rater_db_id=rater.id,
    ):
        raise EvaluationApplicationError(403, "rater_not_assigned_to_packet")

    if hypothesis == Hypothesis.H1:
        normalized = validation.validate_h1_rubric_scores(rubric_scores)
        normalized_rubric_scores = cast("dict[str, float | None]", normalized)
        normalized_section_scores: JsonValue | None = None
        normalized_diagnostics: JsonObject | None = None
        overall_score = mean_score(list(normalized.values()))
    else:
        packet_runtime = await runtime.load_packet_runtime(packet=packet)
        (
            normalized_rubric_scores,
            normalized_section_scores,
            normalized_diagnostics,
            overall_score,
        ) = await validation.validate_h2_scores(
            packet=packet,
            runtime=packet_runtime,
            section_scores=section_scores,
            base_section_scores=base_section_scores,
            diagnostic_scores=diagnostic_scores,
        )

    existing = await persistence.find(
        evaluation_packet_db_id=packet.id,
        rater_db_id=rater.id,
    )
    if existing is not None and hypothesis == Hypothesis.H1:
        raise EvaluationApplicationError(409, "h1_rating_locked")
    now = utc_now()
    rating = (
        RatingRecord(
            id=uuid.uuid4(),
            rating_id=new_public_id(PublicIdPrefix.EVALUATION_RATING),
            evaluation_packet_db_id=packet.id,
            rater_db_id=rater.id,
            hypothesis=hypothesis.value,
            overall_score=overall_score,
            rubric_scores=normalized_rubric_scores,
            section_scores=normalized_section_scores,
            diagnostic_scores=normalized_diagnostics,
            notes=notes,
            created_at=now,
            updated_at=now,
            submitted_at=now,
        )
        if existing is None
        else replace(
            existing,
            hypothesis=hypothesis.value,
            overall_score=overall_score,
            rubric_scores=normalized_rubric_scores,
            section_scores=normalized_section_scores,
            diagnostic_scores=normalized_diagnostics,
            notes=notes,
            updated_at=now,
            submitted_at=now,
        )
    )
    try:
        persisted = await persistence.stage(rating)
        await store.commit()
    except RatingConflictError as exc:
        await store.rollback()
        detail = "h1_rating_locked" if hypothesis == Hypothesis.H1 else "rating_already_submitted"
        raise EvaluationApplicationError(409, detail) from exc
    return _rating_payload(
        persisted, packet_id=packet.evaluation_packet_id, rater_id=rater.rater_id
    )


async def _h2_save_rows(
    *,
    runtime: PacketRuntime,
    ratings: SubmittedRatings,
    validation: RatingValidationService,
    evaluation_packet_id: str,
    submission: H2RatingSubmission,
) -> tuple[list[dict[str, object]] | None, list[dict[str, object]] | None]:
    if submission.candidate_section_scores:
        packet = await packet_or_error(ratings, evaluation_packet_id=evaluation_packet_id)
        context = await runtime.load_packet_runtime(packet=packet)
        primary_run = validation.primary_run_or_error(runtime=context, packet=packet)
        base_run = validation.h2_base_run_or_error(runtime=context, packet=packet)
        p0_run_id = base_run.experiment_condition_run_id
        p1_run_id = primary_run.experiment_condition_run_id
        rows_by_candidate: dict[str, list[dict[str, object]]] = {}
        for entry in submission.candidate_section_scores:
            if entry.candidate_id in rows_by_candidate:
                raise EvaluationApplicationError(422, "h2_candidate_duplicate")
            rows_by_candidate[entry.candidate_id] = _section_rows(entry.section_scores)
        if set(rows_by_candidate) != {p0_run_id, p1_run_id}:
            raise EvaluationApplicationError(422, "h2_candidate_scores_incomplete")
        base_rows = rows_by_candidate[p0_run_id] if p0_run_id != p1_run_id else None
        return rows_by_candidate[p1_run_id], base_rows
    if not submission.section_scores:
        raise EvaluationApplicationError(422, "h2_section_scores_required")
    return (
        _section_rows(submission.section_scores),
        _section_rows(submission.base_section_scores) if submission.base_section_scores else None,
    )


def _section_rows(scores: tuple[H2SectionRating, ...]) -> list[dict[str, object]]:
    return [
        {
            "section_id": score.section_id,
            "learner_state_suitability": score.learner_state_suitability,
            "scaffolding_appropriateness": score.scaffolding_appropriateness,
            "challenge_calibration": score.challenge_calibration,
            "misconception_support": score.misconception_support,
            "objective_preservation": score.objective_preservation,
        }
        for score in scores
    ]


def _rating_payload(
    rating: RatingRecord,
    *,
    packet_id: str,
    rater_id: str,
) -> dict[str, object]:
    return {
        "rating_id": rating.rating_id,
        "evaluation_packet_id": packet_id,
        "rater_id": rater_id,
        "hypothesis": Hypothesis(rating.hypothesis),
        "overall_score": rating.overall_score,
        "rubric_scores": dict(rating.rubric_scores),
        "section_scores": rating.section_scores,
        "diagnostic_scores": rating.diagnostic_scores,
        "notes": rating.notes,
        "created_at": rating.created_at,
        "updated_at": rating.updated_at,
        "submitted_at": rating.submitted_at,
    }
