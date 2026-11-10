"""GET an experiment's record: where its notes came from, who rated them, and the ratings."""

from __future__ import annotations

from dataclasses import asdict
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.domains.experiments.api.deps import study_record_query
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.study_record import StudyRecordQuery
from app.shared.auth import Actor, get_actor
from app.shared.authz import requires
from app.shared.schema_base import UtcDatetime

router = APIRouter(prefix="/experiments", tags=["experiments"])


class DatasetReleaseResponse(BaseModel):
    repo: str
    revision: str
    provenance_sha256: str


class StudySourceResponse(BaseModel):
    datasets: list[DatasetReleaseResponse]
    importer_sha256: str
    imported_at: UtcDatetime


class GenerationRecordResponse(BaseModel):
    hypothesis: str
    model_name: str | None
    prompt_version: str | None
    notes: int


class ProvenanceResponse(BaseModel):
    source: StudySourceResponse | None
    generation: list[GenerationRecordResponse]


class RatedSetResponse(BaseModel):
    part: int
    rater: str
    rater_name: str
    packet: str
    delivery_order: int
    note_id: str
    condition: str | None
    draw: int | None
    other_note_id: str | None
    learner_id: str | None
    state: str
    date_completed: str | None


class ComparedLessonResponse(BaseModel):
    experiment_id: str
    experiment_code: str


class RaterScheduleResponse(BaseModel):
    sets: list[RatedSetResponse]
    compared_lessons: list[ComparedLessonResponse]


class ConditionMeanResponse(BaseModel):
    condition: str
    criterion_id: str
    mean: float
    n: int
    score_counts: list[int]
    double_rated: int
    both_favourable: int


class ChoiceCountResponse(BaseModel):
    criterion_id: str
    favoured: str
    strength: str | None
    count: int


class StudyResultsResponse(BaseModel):
    part_1: list[ConditionMeanResponse]
    part_2: list[ChoiceCountResponse]


class ObjectiveMeanResponse(BaseModel):
    lesson: str
    objective_id: str
    objective_text: str | None
    condition: str
    mean: float
    n: int


class StudyWideResultsResponse(BaseModel):
    part_1: list[ConditionMeanResponse]
    objectives: list[ObjectiveMeanResponse]
    part_2: list[ChoiceCountResponse]


class TranscriptResponse(BaseModel):
    kind: str
    student_id: str | None
    pages: list[dict[str, str]]
    header: dict[str, object]
    body: str
    source_path: str


class LessonDesignResponse(BaseModel):
    experiment_id: str
    objectives: int
    class_notes: int
    learners: int
    part_1_sets: int
    part_2_sets: int


class StudyDesignResponse(BaseModel):
    lessons: list[LessonDesignResponse]
    conditions: list[str]
    draws: int
    raters: int


def _raise_http_error(error: ExperimentApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.get("/{experiment_id}/provenance", response_model=ProvenanceResponse)
async def get_experiment_provenance(
    experiment_id: str,
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
    actor: Actor = Depends(get_actor),
    query: StudyRecordQuery = Depends(study_record_query),
) -> ProvenanceResponse:
    """The release an imported study came from, and the model and prompt behind each note."""
    try:
        provenance = await query.provenance(actor=actor, experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return ProvenanceResponse.model_validate(asdict(provenance))


@router.get("/{experiment_id}/rater-schedule", response_model=RaterScheduleResponse)
async def get_rater_schedule(
    experiment_id: str,
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
    actor: Actor = Depends(get_actor),
    query: StudyRecordQuery = Depends(study_record_query),
) -> RaterScheduleResponse:
    """Who rated the lesson in the study, set by set, and which lessons Part 2 compared."""
    try:
        schedule = await query.schedule(actor=actor, experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return RaterScheduleResponse.model_validate(asdict(schedule))


@router.get("/{experiment_id}/study-results", response_model=StudyResultsResponse)
async def get_study_results(
    experiment_id: str,
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
    actor: Actor = Depends(get_actor),
    query: StudyRecordQuery = Depends(study_record_query),
) -> StudyResultsResponse:
    """The lesson's study ratings described: Part 1 means by condition, Part 2 choices counted."""
    try:
        results = await query.results(actor=actor, experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return StudyResultsResponse.model_validate(asdict(results))


@router.get(
    "/investigations/{investigation_id}/study-results", response_model=StudyWideResultsResponse
)
async def get_study_wide_results(
    investigation_id: str,
    _actor: Actor = Depends(requires(obj="study:*", act="read")),
    query: StudyRecordQuery = Depends(study_record_query),
) -> StudyWideResultsResponse:
    """The study's ratings across its lessons, described, with each objective as a data point."""
    try:
        results = await query.study_results(investigation_id=investigation_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return StudyWideResultsResponse.model_validate(asdict(results))


@router.get("/{experiment_id}/transcripts", response_model=list[TranscriptResponse])
async def get_transcripts(
    experiment_id: str,
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
    actor: Actor = Depends(get_actor),
    query: StudyRecordQuery = Depends(study_record_query),
) -> list[TranscriptResponse]:
    """How the lesson became data: its published transcripts, with the pages each came from."""
    try:
        transcripts = await query.transcripts(actor=actor, experiment_id=experiment_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return [TranscriptResponse.model_validate(asdict(transcript)) for transcript in transcripts]


@router.get("/investigations/{investigation_id}/design", response_model=StudyDesignResponse)
async def get_study_design(
    investigation_id: str,
    _actor: Actor = Depends(requires(obj="study:*", act="read")),
    query: StudyRecordQuery = Depends(study_record_query),
) -> StudyDesignResponse:
    """The study's shape, counted from its record: lessons, objectives, notes, learners, raters."""
    try:
        design = await query.design(investigation_id=investigation_id)
    except ExperimentApplicationError as error:
        _raise_http_error(error)
    return StudyDesignResponse.model_validate(asdict(design))
