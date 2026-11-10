"""The published study imported: read back as content, concluded, and as Part 1 read it."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.concluded_record import is_concluded
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_note_input import (  # noqa: E501
    with_lesson_note,
)
from app.domains.assessments.infrastructure.study_classwork import SqlAlchemyStudyClasswork
from app.domains.assessments.models import StudyClassworkAnswer, StudyClassworkScript
from app.domains.content.domain.types import BuiltIn
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.evaluation.infrastructure.models import EvaluationRater
from app.domains.evaluation.infrastructure.repository import EvaluationRepository
from app.domains.evaluation.infrastructure.study_rating_models import (
    StudyComparativeJudgement,
    StudyCriterionScore,
    StudyRatingDocument,
)
from app.domains.evaluation.infrastructure.study_ratings import SqlAlchemyStudyRatings
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from app.domains.experiments.infrastructure.study_record import SqlAlchemyStudyRecord
from app.domains.experiments.infrastructure.study_transcript_models import StudyTranscript
from app.domains.learners.models import LearnerProfile
from app.domains.teaching.models import LessonPeriod, SchemeOfWork
from app.shared.concluded import ConcludedLessonError
from experiments.study_import.dataset import (
    LESSON_PLANS,
    DatasetMismatchError,
    ReleasedStudy,
)
from experiments.study_import.documents import ReturnedDocument
from experiments.study_import.importer import AlreadyImportedError, import_study
from experiments.study_import.ratings import ObjectiveNames
from experiments.study_import.runs import INVESTIGATION_ID
from migrations.data.content_registry_seed import seed_content_types
from tests.part_1_input import CONDITIONS, RELEASE, part_1_inputs, part_1_request
from tests.study_release import seed_curriculum, write_release


@pytest.fixture
def release(tmp_path: Path) -> ReleasedStudy:
    return ReleasedStudy(write_release(tmp_path))


async def _count(db: AsyncSession, model: type, *where: object) -> int:
    return int(await db.scalar(select(func.count()).select_from(model).where(*where)) or 0)


@pytest.mark.asyncio
async def test_the_study_is_imported_whole_and_once(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)

    report = await import_study(db, release)

    assert (report.lessons, report.lesson_notes, report.learners) == (6, 6, 9)
    assert (report.part_1_notes, report.part_2_notes) == (72, 52)
    assert (report.part_1_scores, report.part_2_judgements) == (2, 1)
    assert await _count(db, ExperimentExecution, ExperimentExecution.hypothesis == "H1") == 18
    assert await _count(db, ExperimentFocalCase) == 26
    assert await _count(db, ExperimentConditionRun) == 72 + 52
    with pytest.raises(AlreadyImportedError):
        await import_study(db, release)


@pytest.mark.asyncio
async def test_a_replaced_study_is_the_study_again_and_nothing_twice(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)

    report = await import_study(db, release, replace=True)

    assert (report.part_1_notes, report.part_2_notes, report.part_1_scores) == (72, 52, 2)
    assert await _count(db, ExperimentConditionRun) == 72 + 52
    assert await _count(db, LessonPeriod) == 6
    assert await _count(db, SchemeOfWork) == 6
    assert await _count(db, LearnerProfile) == 9
    assert await _count(db, StudyClassworkScript) == 1
    assert await is_concluded(db, "LPV-STUDY-t3-w05")


@pytest.mark.asyncio
async def test_only_the_base_the_researcher_approved_and_its_p0s_are_approved(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)
    rows = (
        await db.execute(
            select(
                Artefact.artefact_id,
                Artefact.review_status,
                Artefact.reviewed_by,
                Artefact.artefact_refs,
            ).where(Artefact.experiment_condition_run_id.is_not(None))
        )
    ).all()
    approved = {artefact_id for artefact_id, status, _, _ in rows if status == "approved"}

    assert {reviewer for _, status, reviewer, _ in rows if status == "approved"} == {
        "The study researcher"
    }
    assert {a for a in approved if "-student-" not in a} == {
        f"AT-STUDY-{lesson}-C3-d1"
        for lesson in ("t2-w09", "t3-w02", "t3-w04", "t3-w05", "t3-w06", "t3-w09")
    }
    assert {a for a in approved if "-student-" in a} == {a for a, *_ in rows if a.endswith("-P0")}
    p0 = next(refs for a, _, _, refs in rows if a == "AT-STUDY-t2-w09-student-06-P0")
    assert p0["base_note"] == "AT-STUDY-t2-w09-C3-d1"


@pytest.mark.asyncio
async def test_only_the_objectives_p1_personalised_carry_a_band(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)
    manifests = dict(
        (
            await db.execute(
                select(Artefact.artefact_id, Artefact.manifest).where(
                    Artefact.artefact_id.like("AT-STUDY-t2-w09-student-06-P%")
                )
            )
        ).all()
    )

    def bands(note: str) -> dict[str, str | None]:
        steps = manifests[f"AT-STUDY-t2-w09-student-06-{note}"]["steps"]
        return {step["lesson_objective_id"]: step.get("personalisation_band") for step in steps}

    assert set(bands("P0").values()) == {None}
    assert bands("P1") == {"lo-t2w09-01": "remediate", "lo-t2w09-02": None, "lo-t2w09-03": None}


@pytest.mark.asyncio
async def test_an_imported_lesson_is_the_teachers_content_concluded_and_read_only(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await (await db.connection()).run_sync(seed_content_types)
    await import_study(db, release)

    content = await SqlAlchemyContentRecords().find(
        db, plan_version_id="LPV-STUDY-t3-w05", type=None, level=None, student_id=None
    )

    assert {(r.type, r.provenance.get("origin"), r.read_only) for r in content} == {
        (BuiltIn.LESSON_PLAN.value, "study_record", True),
        (BuiltIn.LESSON_NOTE.value, "study_record", True),
    }
    assert await is_concluded(db, "LPV-STUDY-t3-w05")
    note = (
        await db.execute(select(Artefact).where(Artefact.artefact_id == "AT-STUDY-t3-w05-note"))
    ).scalar_one()
    note.manifest = {"sections": []}
    with pytest.raises(ConcludedLessonError):
        await db.flush()


@pytest.mark.asyncio
async def test_the_study_runs_keep_the_pipeline_each_note_was_written_by(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)

    rows = (
        await db.execute(
            select(Artefact.scope, Artefact.student_id, Artefact.artefact_refs).where(
                Artefact.experiment_condition_run_id.is_not(None)
            )
        )
    ).all()
    by = {(scope, refs["study"]["condition"], refs["pipeline"]) for scope, _, refs in rows}

    assert by == {
        *(("class_level", c, "2026-08-25") for c in ("C0", "C1", "C2", "C3")),
        ("learner_level", "P0", "2026-08-25"),
        ("learner_level", "P1", "2026-09-02"),
    }
    assert {student for scope, student, _ in rows if scope == "learner_level"} == {
        f"ST-STUDY-0{n}" for n in range(1, 10)
    }


@pytest.mark.asyncio
async def test_a_lesson_read_back_from_the_database_is_the_input_part_1_read(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)
    part_1 = part_1_inputs()

    for lesson in part_1:
        plan = await db.scalar(
            select(PlanVersion.session_plan).where(PlanVersion.version_id == f"LPV-STUDY-{lesson}")
        )
        note = await db.scalar(
            select(Artefact.manifest).where(Artefact.artefact_id == f"AT-STUDY-{lesson}-note")
        )
        rebuilt = with_lesson_note(plan, {s["step_id"]: s["body"] for s in note["sections"]})
        for condition in CONDITIONS:
            assert part_1_request(rebuilt, condition) == part_1_request(
                part_1[lesson], condition
            ), lesson


@pytest.mark.asyncio
async def test_each_rating_is_kept_in_the_studys_terms_against_the_note_it_rated(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)

    scores = (await db.execute(select(StudyCriterionScore))).scalars().all()
    [judgement] = (await db.execute(select(StudyComparativeJudgement))).scalars().all()

    assert {(s.artefact_id, s.criterion_id, s.score, s.comment) for s in scores} == {
        ("AT-STUDY-t3-w05-C2-d3", "curriculum_objective_alignment", 4, "Covers."),
        ("AT-STUDY-t3-w05-C2-d3", "instructional_quality", 5, None),
    }
    assert (judgement.artefact_a_id, judgement.artefact_b_id) == (
        "AT-STUDY-t2-w09-student-01-P0",
        "AT-STUDY-t2-w09-student-01-P1",
    )
    assert (judgement.criterion_id, judgement.choice, judgement.favoured_condition) == (
        "adaptive_calibration",
        "B clearly better",
        "P1",
    )
    judgement.comment = "edited"
    with pytest.raises(ConcludedLessonError):
        await db.flush()


@pytest.mark.skipif(
    not (RELEASE / LESSON_PLANS).is_dir(), reason="the published datasets are not here"
)
@pytest.mark.asyncio
async def test_the_published_study_imports_every_rating(db: AsyncSession) -> None:
    await seed_curriculum(db)

    report = await import_study(db, ReleasedStudy(RELEASE))

    assert (report.part_1_scores, report.part_2_judgements) == (1212, 199)


@pytest.mark.asyncio
async def test_a_notes_ratings_read_back_from_either_side_of_a_comparison(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)
    reader = SqlAlchemyStudyRatings()

    part_1 = await reader.for_note(db, "AT-STUDY-t3-w05-C2-d3")
    p0 = await reader.for_note(db, "AT-STUDY-t2-w09-student-01-P0")
    p1 = await reader.for_note(db, "AT-STUDY-t2-w09-student-01-P1")

    assert [score.score for score in part_1.scores] == [4, 5]
    assert part_1.scores[0].objective_text == "identify properties of cylinders and spheres"
    assert [(d.shown_as, d.state, d.closing_comment) for d in part_1.documents] == [
        (None, "partial", "Clear throughout.")
    ]
    assert p1.judgements[0].objective_text == "carry out order of operation in algebra"
    assert [d.shown_as for d in p1.documents] == ["B"]
    assert (p0.judgements[0].shown_as, p0.judgements[0].other_note_id) == (
        "A",
        "AT-STUDY-t2-w09-student-01-P1",
    )
    assert (p1.judgements[0].shown_as, p1.judgements[0].favoured_condition) == ("B", "P1")
    tallies = await reader.tally(db, ["LPV-STUDY-t3-w05", "LPV-STUDY-t2-w09", "LPV-STUDY-t3-w02"])
    assert [(t.plan_version_id, t.scores, t.judgements, t.raters) for t in tallies] == [
        ("LPV-STUDY-t3-w05", 2, 0, 1),
        ("LPV-STUDY-t2-w09", 0, 1, 1),
    ]


@pytest.mark.asyncio
async def test_a_lessons_rater_schedule_names_each_set_and_what_it_rated(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    await import_study(db, release)
    reader = SqlAlchemyStudyRecord(db)

    part_1 = await reader.schedule("LPV-STUDY-t3-w05")
    part_2 = await reader.schedule("LPV-STUDY-t3-w02")
    unrated = await reader.schedule("LPV-STUDY-t3-w06")

    assert [(s.part, s.rater_name, s.condition, s.draw, s.learner_id) for s in part_1.sets] == [
        (1, "Study rater 2", "C2", 3, None)
    ]
    assert [
        (s.rater_name, s.condition, s.other_note_id, s.learner_id, s.state) for s in part_2.sets
    ] == [("Study rater 4", "P1", "AT-STUDY-t3-w02-student-07-P0", "ST-STUDY-07", "untouched")]
    assert unrated.sets == []
    part_1_results = await reader.results("LPV-STUDY-t3-w05")
    part_2_results = await reader.results("LPV-STUDY-t2-w09")
    assert [(m.condition, m.n) for m in part_1_results.part_1] == [("C2", 1), ("C2", 1)]
    assert [(c.favoured, c.count) for c in part_2_results.part_2] == [("P1", 1)]
    assert [lesson.experiment_code for lesson in unrated.compared_lessons] == [
        "study-t2-w09",
        "study-t3-w02",
    ]


@pytest.mark.asyncio
async def test_an_imported_lessons_provenance_names_its_release_and_what_wrote_its_notes(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    pins = {"ng-jss1-math-lesson-plans": {"revision": "abc123", "provenance_sha256": "f" * 64}}
    record = StudyImport(investigation_id=INVESTIGATION_ID, release=pins, importer="e" * 64)
    await import_study(db, release, record=record)
    experiment = (
        await db.execute(select(Experiment).where(Experiment.experiment_code == "study-t3-w05"))
    ).scalar_one()

    provenance = await SqlAlchemyStudyRecord(db).provenance(
        experiment_db_id=experiment.id, investigation_db_id=experiment.investigation_db_id
    )

    assert provenance.source is not None
    assert [(d.repo, d.revision) for d in provenance.source.datasets] == [
        ("tosinamuda/ng-jss1-math-lesson-plans", "abc123")
    ]
    assert provenance.source.importer_sha256 == "e" * 64
    assert [(r.hypothesis, r.prompt_version, r.notes) for r in provenance.generation] == [
        ("H1", "2026-08-25", 12),
        ("H2", "2026-08-25", 9),
        ("H2", "2026-09-02", 9),
    ]
    assert {r.model_name for r in provenance.generation} == {"openai/deepseek-v4-flash"}


@pytest.mark.asyncio
async def test_each_lessons_transcripts_are_kept_as_published_with_their_pages(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    report = await import_study(db, release)
    rows = (await db.execute(select(StudyTranscript))).scalars().all()
    by_path = {row.source_path.removeprefix("transcripts/"): row for row in rows}

    assert report.transcripts == 4
    assert set(by_path) == {
        "t3-w05/teacher.md",
        "t3-w05/teacher-cleaned.md",
        "t3-w05/_cleaning-log.md",
        "t2-w09/student-01.md",
    }
    teacher = by_path["t3-w05/teacher.md"]
    assert (teacher.kind, teacher.plan_version_id) == ("teacher_record", "LPV-STUDY-t3-w05")
    assert teacher.pages == [
        {"file": "lesson-plan-01.jpeg", "role": "plan_header"},
        {"file": "lesson-plan-02.jpeg", "role": "step_i"},
    ]
    assert teacher.body == "Objectives: (iii) calculate capacity\n"
    assert by_path["t3-w05/teacher-cleaned.md"].header["cleaned"][0]["change"] == "dropped (iii)"
    script = by_path["t2-w09/student-01.md"]
    assert (script.kind, script.student_id) == ("learner_script", "ST-STUDY-01")
    assert script.pages == [{"file": "classwork-01.jpeg", "role": "script"}]
    assert script.header["teacher_mark_date"] == "2026-05-21"
    script.body = "edited"
    with pytest.raises(ConcludedLessonError):
        await db.flush()


@pytest.mark.asyncio
async def test_a_learners_classwork_is_kept_as_marked_and_read_back(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    report = await import_study(db, release)

    classwork = await SqlAlchemyStudyClasswork().for_learner(db, "LPV-STUDY-t2-w09", "ST-STUDY-06")
    absent = await SqlAlchemyStudyClasswork().for_learner(db, "LPV-STUDY-t2-w09", "ST-STUDY-04")

    assert report.classwork_scripts == 1
    assert [(q.n, q.lesson_objective_id, q.answer) for q in classwork.questions] == [
        (1, "lo-t2w09-01", "$34n$")
    ]
    assert classwork.script is not None
    [answer] = classwork.script.answers
    assert (classwork.script.teacher_total, answer.mark, answer.misconception_code) == (
        "0/1",
        "incorrect",
        "adds_before_multiplying",
    )
    assert absent.script is None
    row = (await db.execute(select(StudyClassworkAnswer))).scalar_one()
    row.mark = "correct"
    with pytest.raises(ConcludedLessonError):
        await db.flush()


@pytest.mark.asyncio
async def test_every_returned_set_is_kept_answered_or_not_with_its_rater(
    db: AsyncSession, release: ReleasedStudy
) -> None:
    await seed_curriculum(db)
    report = await import_study(db, release)
    documents = (await db.execute(select(StudyRatingDocument))).scalars().all()
    raters = {
        r.id: r
        for r in (
            await db.execute(
                select(EvaluationRater).where(EvaluationRater.origin == "study_record")
            )
        ).scalars()
    }
    [judgement] = (await db.execute(select(StudyComparativeJudgement))).scalars().all()

    assert (report.rating_documents, report.closing_comments, report.raters) == (3, 1, 3)
    assert {
        (d.packet, d.state, d.rows_unanswered, d.artefact_a_id, d.artefact_b_id, d.closing_comment)
        for d in documents
    } == {
        ("h1-pkt-010", "partial", 4, "AT-STUDY-t3-w05-C2-d3", None, "Clear throughout."),
        (
            "h2-pkt-004",
            "partial",
            2,
            "AT-STUDY-t2-w09-student-01-P0",
            "AT-STUDY-t2-w09-student-01-P1",
            None,
        ),
        (
            "h2-pkt-012",
            "untouched",
            6,
            "AT-STUDY-t3-w02-student-07-P1",
            "AT-STUDY-t3-w02-student-07-P0",
            None,
        ),
    }
    assert {raters[d.rater_db_id].display_name for d in documents} == {
        "Study rater 1",
        "Study rater 2",
        "Study rater 4",
    }
    assert raters[judgement.rater_db_id].rater_id == "STUDY-rater-1"
    assert all(rater.user_id is None for rater in raters.values())
    assert await EvaluationRepository(db).list_raters() == []
    assert judgement.lesson_objective_id == "lo-t2w09-01"


def test_a_page_names_its_objective_however_the_maths_was_typeset() -> None:
    names = ObjectiveNames(
        {
            "t3-w06": {
                "lesson_plan_objectives": [
                    {"lesson_objective_id": "lo-a", "objective_text": "construct parallel lines"},
                    {
                        "lesson_objective_id": "lo-90",
                        "objective_text": "construct angle $90^\\circ$",
                    },
                    {
                        "lesson_objective_id": "lo-60",
                        "objective_text": "construct angle $60^\\circ$",
                    },
                ]
            }
        }
    )
    document = ReturnedDocument({1: "construct angle 60∘", 2: "construct angle 90∘"})
    row = {"lesson": "t3-w06", "document": "d.docx", "objective_index": "2"}

    assert names.on_page(row, {"d.docx": document}) == "lo-90"
    with pytest.raises(DatasetMismatchError, match="not an objective of t3-w06"):
        names.on_page({**row, "objective_index": "3"}, {"d.docx": document})
