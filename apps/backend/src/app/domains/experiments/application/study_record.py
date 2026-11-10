"""An ended experiment's record: where its notes came from, who rated them, and the ratings.

For an experiment imported from the published MSc study, the record reaches back to the
release it was imported from and to the rating documents its raters returned.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.domains.evaluation.application.study_results import LessonResults, StudyResults
from app.domains.experiments.application.authorization import (
    ExperimentAccessReader,
    ExperimentAuthorization,
)
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.shared.auth import Actor


@dataclass(frozen=True)
class DatasetRelease:
    """One published dataset, at the Hub commit the study was imported from."""

    repo: str
    revision: str
    provenance_sha256: str


@dataclass(frozen=True)
class StudySource:
    """The published release an imported study came from, and the importer that read it."""

    datasets: list[DatasetRelease]
    importer_sha256: str
    imported_at: datetime


@dataclass(frozen=True)
class GenerationRecord:
    """The model and prompt version that wrote some of a hypothesis's notes."""

    hypothesis: str
    model_name: str | None
    prompt_version: str | None
    notes: int


@dataclass(frozen=True)
class Provenance:
    #: Set for an experiment imported from the published study; none for one run in the app.
    source: StudySource | None
    generation: list[GenerationRecord]


@dataclass(frozen=True)
class RatedSet:
    """One rating document a study rater returned for a lesson: whom it rated, and how fully."""

    #: 1 scored one class note; 2 compared one learner's two notes.
    part: int
    rater: str
    rater_name: str
    packet: str
    #: Where the set sat in the rater's pile, from 1.
    delivery_order: int
    #: The note the set rated, or in Part 2 the note shown as A.
    note_id: str
    #: That note's condition, e.g. C2 or P1, and the draw that wrote it.
    condition: str | None
    draw: int | None
    #: The learner's other note, shown as B, for Part 2.
    other_note_id: str | None
    #: The learner whose notes a Part 2 set compared.
    learner_id: str | None
    state: str
    #: As the rater wrote it on the document.
    date_completed: str | None


@dataclass(frozen=True)
class ComparedLesson:
    """A lesson whose learner notes the study's Part 2 compared."""

    experiment_id: str
    experiment_code: str


@dataclass(frozen=True)
class RaterSchedule:
    """Who rated a lesson in the study, set by set, and which lessons Part 2 compared."""

    sets: list[RatedSet]
    compared_lessons: list[ComparedLesson]


@dataclass(frozen=True)
class Transcript:
    """One published transcript of a lesson: what it records, the pages it came from, its text."""

    kind: str
    student_id: str | None
    pages: list[dict[str, str]]
    header: dict[str, object]
    body: str
    source_path: str


@dataclass(frozen=True)
class LessonDesign:
    """One lesson's share of the study: its objectives, notes, learners and rating sets."""

    experiment_id: str
    objectives: int
    class_notes: int
    learners: int
    part_1_sets: int
    part_2_sets: int


@dataclass(frozen=True)
class StudyDesign:
    """The study's shape, counted from its record rather than stated."""

    lessons: list[LessonDesign]
    conditions: list[str]
    draws: int
    raters: int


class StudyRecordReader(Protocol):
    async def provenance(
        self, *, experiment_db_id: uuid.UUID, investigation_db_id: uuid.UUID
    ) -> Provenance: ...

    async def schedule(self, plan_version_id: str) -> RaterSchedule: ...

    async def results(self, plan_version_id: str) -> LessonResults: ...

    async def study_results(self, investigation_id: str) -> StudyResults | None: ...

    async def transcripts(self, plan_version_id: str) -> list[Transcript]: ...

    async def design(self, investigation_id: str) -> StudyDesign | None: ...


class StudyRecordQuery:
    """Read an experiment's record for a caller allowed to read the experiment."""

    def __init__(self, access: ExperimentAccessReader, reader: StudyRecordReader) -> None:
        self._authorization = ExperimentAuthorization(access)
        self._reader = reader

    async def provenance(self, *, actor: Actor, experiment_id: str) -> Provenance:
        experiment = await self._authorization.load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        return await self._reader.provenance(
            experiment_db_id=experiment.id, investigation_db_id=experiment.investigation_db_id
        )

    async def schedule(self, *, actor: Actor, experiment_id: str) -> RaterSchedule:
        experiment = await self._authorization.load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        return await self._reader.schedule(experiment.plan_version_id or "")

    async def results(self, *, actor: Actor, experiment_id: str) -> LessonResults:
        experiment = await self._authorization.load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        return await self._reader.results(experiment.plan_version_id or "")

    async def study_results(self, *, investigation_id: str) -> StudyResults:
        results = await self._reader.study_results(investigation_id)
        if results is None:
            raise ExperimentApplicationError(404, "investigation_not_found")
        return results

    async def transcripts(self, *, actor: Actor, experiment_id: str) -> list[Transcript]:
        experiment = await self._authorization.load_and_authorize_experiment(
            actor=actor, experiment_id=experiment_id
        )
        return await self._reader.transcripts(experiment.plan_version_id or "")

    async def design(self, *, investigation_id: str) -> StudyDesign:
        design = await self._reader.design(investigation_id)
        if design is None:
            raise ExperimentApplicationError(404, "investigation_not_found")
        return design
