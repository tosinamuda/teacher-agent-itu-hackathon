"""Import the released study in one transaction, then conclude it: all of it, or none."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.assessments.models import StudyClassworkScript
from app.domains.experiments.infrastructure.models import Investigation
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from app.shared.time import utc_now
from experiments.study_import.classwork import classwork_rows
from experiments.study_import.dataset import ReleasedStudy
from experiments.study_import.lessons import (
    ImportedLesson,
    learner_rows,
    lesson_note_row,
    plan_rows,
    plan_version_id,
)
from experiments.study_import.raters import rater_rows
from experiments.study_import.ratings import (
    ObjectiveNames,
    part_1_scores,
    part_2_judgements,
    part_2_notes,
    rating_documents,
)
from experiments.study_import.runs import (
    INVESTIGATION_ID,
    Staged,
    experiment_row,
    investigation_row,
    part_1_rows,
    part_2_rows,
)
from experiments.study_import.school import place_lessons, study_class
from experiments.study_import.transcript_rows import transcript_rows
from experiments.study_import.withdraw import withdraw_study


def zip_stages(*runs: Staged) -> list[list[Any]]:
    """The runs' rows, stage by stage: every run's parents, then every run's runs, then notes."""
    return [sum((list(run.stages[index]) for run in runs), []) for index in range(3)]


class AlreadyImportedError(RuntimeError):
    """The study is in the database already; a concluded study is never imported twice."""


@dataclass(frozen=True)
class ImportReport:
    lessons: int
    lesson_notes: int
    learners: int
    part_1_notes: int
    part_2_notes: int
    part_1_scores: int
    part_2_judgements: int
    classwork_scripts: int
    transcripts: int
    rating_documents: int
    closing_comments: int
    raters: int


async def import_study(
    db: AsyncSession,
    study: ReleasedStudy,
    *,
    commit: bool = True,
    replace: bool = False,
    record: StudyImport | None = None,
) -> ImportReport:
    """Write the study, conclude every lesson in it, and commit — or, with ``commit=False``,
    write it all and roll it back, so a dry run exercises exactly what an import does.

    ``replace`` first withdraws a study already imported, in the same transaction, so a
    corrected import takes its place whole or not at all. ``record`` says which release and
    importer wrote it.
    """
    if replace:
        await withdraw_study(db)
    if await db.scalar(
        select(Investigation.id).where(Investigation.investigation_id == INVESTIGATION_ID)
    ):
        raise AlreadyImportedError(f"{INVESTIGATION_ID} is already imported; --replace replaces it")
    lessons, part_1, part_2 = study.lessons(), study.part_1(), study.part_2()
    places = await place_lessons(db, lessons)
    pseudonyms = {case["student"] for case in part_2["cases"]}
    klass = await study_class(db)
    imported = {
        lesson.lesson: ImportedLesson(lesson, places[lesson.lesson], plan_version_id(lesson.lesson))
        for lesson in lessons
    }
    investigation = investigation_row()
    learners: dict[str, set[str]] = defaultdict(set)
    for case in part_2["cases"]:
        learners[case["lesson"]].add(case["student"])
    experiments = {
        name: experiment_row(investigation, lesson, sorted(learners[name]))
        for name, lesson in imported.items()
    }
    part_1_staged = part_1_rows(part_1, imported, experiments, part_2["base"])
    part_2_staged = part_2_rows(part_2, imported, experiments)
    plans = [plan_rows(lesson, places[lesson.lesson]) for lesson in lessons]
    transcripts = [
        row
        for lesson in lessons
        for row in transcript_rows(study.transcripts(lesson.lesson), plan_version_id(lesson.lesson))
    ]
    classwork = [
        classwork_rows(found, plan_version_id(lesson.lesson))
        for lesson in lessons
        if (found := study.classwork(lesson.lesson)) is not None
    ]
    part_1_rated, part_2_rated = study.part_1_ratings(), study.part_2_judgements()
    index = study.document_index()
    raters = rater_rows(row["rater"] for row in index)
    documents = study.returned_documents(
        {row["document"] for row in (*part_1_rated, *part_2_rated)}
    )
    objectives = ObjectiveNames({lesson.lesson: lesson.plan for lesson in lessons})
    scores = part_1_scores(part_1_rated, documents, objectives, raters)
    judgements = part_2_judgements(part_2_rated, documents, objectives, raters)
    returned = rating_documents(
        index, part_1_rated, part_2_notes(study.part_2_allocation(), part_2_rated), raters
    )
    stages: list[list[Any]] = [
        [
            *learner_rows(pseudonyms, klass.id),
            investigation,
            *(plan for plan, _ in plans),
            *raters.values(),
        ],
        [version for _, version in plans],
        transcripts,
        [lesson_note_row(lesson) for lesson in lessons if lesson.note_sections],
        [row for parents, _ in classwork for row in parents],
        [answer for _, answers in classwork for answer in answers],
        list(experiments.values()),
        *zip_stages(part_1_staged, part_2_staged),
        [*scores, *judgements, *returned, *([record] if record else [])],
    ]
    for stage in stages:
        db.add_all(stage)
        await db.flush()

    concluded_at = utc_now()
    versions = await db.execute(
        select(PlanVersion).where(
            PlanVersion.version_id.in_([lesson.plan_version_id for lesson in imported.values()])
        )
    )
    for version in versions.scalars():
        version.concluded_at = concluded_at
    await db.flush()

    report = ImportReport(
        lessons=len(imported),
        lesson_notes=sum(1 for lesson in lessons if lesson.note_sections),
        learners=len(pseudonyms),
        part_1_notes=len(part_1_staged.notes),
        part_2_notes=len(part_2_staged.notes),
        part_1_scores=len(scores),
        part_2_judgements=len(judgements),
        rating_documents=len(returned),
        raters=len(raters),
        closing_comments=sum(1 for document in returned if document.closing_comment),
        transcripts=len(transcripts),
        classwork_scripts=sum(
            isinstance(row, StudyClassworkScript) for parents, _ in classwork for row in parents
        ),
    )
    if commit:
        await db.commit()
    else:
        await db.rollback()
    return report
