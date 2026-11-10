"""The evaluation's class results are brought onto a lesson, and refused where they do not fit."""

from __future__ import annotations

import json
import uuid

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
    PlanVersionObjective,
)
from app.domains.assessments.models import (
    ExitTicketSubmission,
    StudyClassworkAnswer,
    StudyClassworkQuestion,
    StudyClassworkScript,
)
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.learners.models.learner import LearnerProfile
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.application.learner_answers import LearnerAnswers
from app.domains.teaching.application.sequence_service import TeachingSequenceApplicationError
from app.domains.teaching.application.study_results_service import StudyResultsService
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace
from app.domains.teaching.schemas import StandInPairRequest

pytestmark = pytest.mark.asyncio

STUDY = "V-STUDY"
TARGET = "V-TARGET"


def _lesson(title: str, plan: str, version: str, period: uuid.UUID) -> list[object]:
    return [
        LessonPlan(
            plan_id=plan,
            lesson_period_id=period,
            title=title,
            subject="Mathematics",
            track="General",
            grade="JSS1",
        ),
        PlanVersion(
            version_id=version,
            plan_id=plan,
            source_type="generated",
            session_plan={},
            status=PlanVersionStatus.APPROVED,
        ),
    ]


def _objectives(version: str, *ids: str) -> list[object]:
    return [
        PlanVersionObjective(
            plan_version_id=version,
            lesson_objective_id=objective,
            objective_text=f"Text of {objective}",
            objective_order=at,
        )
        for at, objective in enumerate(ids, start=1)
    ]


async def _seed(db: AsyncSession, *, target_objectives: tuple[str, ...] = ("lo1", "lo2")):  # type: ignore[no-untyped-def]
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    offering, workspace, week = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    target_period, study_period = uuid.uuid4(), uuid.uuid4()
    db.add_all(
        [
            TermClassSubject(
                id=offering, course_id=uuid.uuid4(), class_id=uuid.uuid4(), term="1st", year="y"
            ),
            TeacherWorkspace(id=workspace, term_class_subject_id=offering, teacher_id=uuid.uuid4()),
            SchemeOfWork(id=week, term_class_subject_id=offering, week_number=1, title="W"),
            LessonPeriod(id=target_period, scheme_of_work_id=week, period_number=1),
            LessonPeriod(id=study_period, scheme_of_work_id=week, period_number=2),
            *_lesson("Target", "P-TARGET", TARGET, target_period),
            *_lesson("Study lesson", "P-STUDY", STUDY, study_period),
            *_objectives(TARGET, *target_objectives),
            *_objectives(STUDY, "lo1", "lo2"),
            Experiment(
                experiment_id="E-STUDY",
                experiment_code="E-STUDY",
                investigation_db_id=uuid.uuid4(),
                teacher_workspace_id=workspace,
                plan_version_id=STUDY,
            ),
            LearnerProfile(student_id="S-1", full_name="Ada", grade="JSS1", track="General"),
            LearnerProfile(student_id="S-2", full_name="Bola", grade="JSS1", track="General"),
        ]
    )
    await db.flush()
    for n, objective in enumerate(("lo1", "lo1", "lo2", "lo2"), start=1):
        db.add(
            StudyClassworkQuestion(
                plan_version_id=STUDY,
                assessed_set="set",
                question_n=n,
                lesson_objective_id=objective,
                text=f"Question {n}",
            )
        )
    for student, marks in (
        ("S-1", ["correct"] * 4),
        ("S-2", ["correct", "correct", "incorrect", "incorrect"]),
    ):
        script = StudyClassworkScript(
            id=uuid.uuid4(),
            plan_version_id=STUDY,
            student_id=student,
            teacher_total="?",
            capture_complete=True,
        )
        db.add(script)
        await db.flush()
        for n, mark in enumerate(marks, start=1):
            db.add(
                StudyClassworkAnswer(
                    script_id=script.id,
                    plan_version_id=STUDY,
                    question_n=n,
                    mark=mark,
                    uncertain=False,
                    working="",
                    misconception_code="M-X" if mark == "incorrect" else None,
                )
            )
    await db.flush()
    return workspace, target_period, study_period


async def test_the_sources_are_the_lessons_of_the_evaluation_with_marked_scripts(
    db: AsyncSession,
) -> None:
    await _seed(db)

    sources = await StudyResultsService().sources(db)

    assert [(s.plan_version_id, s.lesson_title, s.learners) for s in sources] == [
        (STUDY, "Study lesson", 2)
    ]


async def test_importing_copies_the_marks_and_each_learner_is_placed_by_their_weakest_objective(
    db: AsyncSession,
) -> None:
    workspace, target, _ = await _seed(db)
    service = StudyResultsService()
    assert (await service.results(db, workspace, target)).imported is False

    results = await service.import_results(db, workspace, target, STUDY)

    assert results.imported is True
    assert [(r.full_name, r.band, r.correct, r.out_of) for r in results.learners] == [
        ("Bola", "remediate", 2, 4),
        ("Ada", "extend", 4, 4),
    ]
    bola = results.learners[0]
    weak = next(o for o in bola.objectives if o.lesson_objective_id == "lo2")
    assert (weak.objective_text, weak.correct, weak.out_of, weak.misconceptions) == (
        "Text of lo2",
        0,
        2,
        ["M-X"],
    )


async def test_the_same_results_are_not_imported_twice(db: AsyncSession) -> None:
    workspace, target, _ = await _seed(db)
    service = StudyResultsService()
    await service.import_results(db, workspace, target, STUDY)

    with pytest.raises(TeachingSequenceApplicationError) as refused:
        await service.import_results(db, workspace, target, STUDY)

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "class_results_already_imported",
    )


async def test_results_marked_against_objectives_the_plan_lacks_are_refused(
    db: AsyncSession,
) -> None:
    workspace, target, _ = await _seed(db, target_objectives=("lo1",))

    with pytest.raises(TeachingSequenceApplicationError) as refused:
        await StudyResultsService().import_results(db, workspace, target, STUDY)

    assert (refused.value.status_code, refused.value.detail) == (
        422,
        "the_plan_lacks_the_objectives:lo2",
    )


async def test_a_source_without_results_and_a_lesson_outside_the_class_are_refused(
    db: AsyncSession,
) -> None:
    workspace, target, _ = await _seed(db)
    service = StudyResultsService()

    with pytest.raises(TeachingSequenceApplicationError) as no_source:
        await service.import_results(db, workspace, target, "V-NOWHERE")
    with pytest.raises(TeachingSequenceApplicationError) as outside:
        await service.results(db, workspace, uuid.uuid4())

    assert no_source.value.detail == "study_results_not_found"
    assert outside.value.detail == "workspace_or_lesson_not_found"


async def test_a_class_learner_takes_a_study_learners_marks_as_their_own_results(
    db: AsyncSession,
) -> None:
    workspace, target_period, _ = await _seed(db)
    service = StudyResultsService()
    await service.import_results(db, workspace, target_period, STUDY)

    made = await service.stand_in(
        db,
        workspace,
        target_period,
        [StandInPairRequest(student_id="S-2", study_student_id="S-1")],
        "Teacher",
    )

    assert [(m.student_id, m.study_student_id) for m in made.made] == [("S-2", "S-1")]
    submission = await db.scalar(
        select(ExitTicketSubmission).where(
            ExitTicketSubmission.student_id == "S-2", ExitTicketSubmission.plan_version_id == TARGET
        )
    )
    assert submission is not None
    assert {o["lesson_objective_id"]: o["score"] for o in submission.results["objectives"]} == {
        "lo1": 2,
        "lo2": 2,
    }
    assert submission.entered_by == "Teacher · marks of Ada"


async def test_stand_ins_wait_for_the_class_results_to_be_imported(db: AsyncSession) -> None:
    workspace, target_period, _ = await _seed(db)

    with pytest.raises(TeachingSequenceApplicationError) as refused:
        await StudyResultsService().stand_in(
            db,
            workspace,
            target_period,
            [StandInPairRequest(student_id="S-2", study_student_id="S-1")],
            None,
        )

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "import_the_class_results_first",
    )


async def test_a_study_learner_with_nothing_marked_cannot_stand_in(db: AsyncSession) -> None:
    workspace, target_period, _ = await _seed(db)
    service = StudyResultsService()
    await service.import_results(db, workspace, target_period, STUDY)

    with pytest.raises(TeachingSequenceApplicationError) as refused:
        await service.stand_in(
            db,
            workspace,
            target_period,
            [StandInPairRequest(student_id="S-2", study_student_id="S-NONE")],
            None,
        )

    assert (refused.value.status_code, refused.value.detail) == (422, "nothing_marked:S-NONE")


async def test_a_lesson_the_marks_were_only_copied_onto_is_not_a_source(db: AsyncSession) -> None:
    workspace, target_period, _ = await _seed(db)
    service = StudyResultsService()
    await service.import_results(db, workspace, target_period, STUDY)

    sources = await service.sources(db)

    assert [s.plan_version_id for s in sources] == [STUDY]


async def test_a_source_that_fits_neither_for_its_marks_nor_for_its_note_is_not_offered(
    db: AsyncSession,
) -> None:
    _, target_period, _ = await _seed(db, target_objectives=("lo1",))

    sources = await StudyResultsService().sources(db, target_period)

    assert sources == []


async def test_a_source_whose_note_fits_is_offered_though_its_marks_do_not(
    db: AsyncSession,
) -> None:
    _, target_period, _ = await _seed(db, target_objectives=("lo1",))
    await _with_note(db, plan_steps=["s1"], note_steps=["s1"])

    sources = await StudyResultsService().sources(db, target_period)

    assert [(s.plan_version_id, s.fits, s.note_fits) for s in sources] == [(STUDY, False, True)]


async def test_a_source_whose_objectives_the_plan_has_is_marked_as_fitting(
    db: AsyncSession,
) -> None:
    _, target_period, _ = await _seed(db)

    sources = await StudyResultsService().sources(db, target_period)

    assert [(s.plan_version_id, s.fits) for s in sources] == [(STUDY, True)]


async def _with_note(
    db: AsyncSession,
    *,
    plan_steps: list[str],
    note_steps: list[str],
    evaluation_steps: tuple[str, ...] = (),
) -> None:
    """The evaluation lesson has an approved note; the target's plan has these steps."""
    await db.execute(
        text("UPDATE plan_versions SET session_plan = :plan WHERE version_id = :version"),
        {
            "plan": json.dumps(
                {
                    "steps": [
                        {
                            "step_id": step,
                            "step_kind": "evaluation" if step in evaluation_steps else "core",
                        }
                        for step in plan_steps
                    ]
                }
            ),
            "version": TARGET,
        },
    )
    db.add(
        Artefact(
            artefact_id="AT-NOTE",
            artefact_type="lesson_note",
            scope="class_level",
            plan_version_id=STUDY,
            manifest={
                "sections": [{"step_id": step, "body": f"Body of {step}"} for step in note_steps]
            },
            artefact_refs={},
            version=1,
            review_status="approved",
        )
    )
    await db.flush()


async def test_an_evaluation_lesson_offers_its_approved_note_when_it_covers_every_step(
    db: AsyncSession,
) -> None:
    _, target_period, _ = await _seed(db)
    await _with_note(db, plan_steps=["s1", "s2"], note_steps=["s1", "s2", "s3"])

    source = (await StudyResultsService().sources(db, target_period))[0]

    assert (source.lesson_note_id, source.note_fits) == ("AT-NOTE", True)


async def test_an_evaluation_note_that_lacks_a_step_of_the_plan_is_marked_as_not_fitting(
    db: AsyncSession,
) -> None:
    _, target_period, _ = await _seed(db)
    await _with_note(db, plan_steps=["s1", "s2"], note_steps=["s1"])

    source = (await StudyResultsService().sources(db, target_period))[0]

    assert (source.lesson_note_id, source.note_fits) == ("AT-NOTE", False)


async def test_only_the_evaluations_own_lessons_are_known_as_such(db: AsyncSession) -> None:
    await _seed(db)
    service = StudyResultsService()

    assert await service.is_evaluation_lesson(db, STUDY) is True
    assert await service.is_evaluation_lesson(db, TARGET) is False


async def test_an_evaluation_step_needs_no_section_in_the_note_for_it_to_fit(
    db: AsyncSession,
) -> None:
    _, target_period, _ = await _seed(db)
    await _with_note(db, plan_steps=["s1", "s2"], note_steps=["s1"], evaluation_steps=("s2",))

    source = (await StudyResultsService().sources(db, target_period))[0]

    assert source.note_fits is True


async def test_a_stand_in_learner_shows_every_question_the_study_learner_was_marked_on(
    db: AsyncSession,
) -> None:
    workspace, target_period, _ = await _seed(db)
    service = StudyResultsService()
    await service.import_results(db, workspace, target_period, STUDY)
    await service.stand_in(
        db,
        workspace,
        target_period,
        [StandInPairRequest(student_id="S-2", study_student_id="S-1")],
        "Teacher",
    )

    seen = await LearnerAnswers().of(db, workspace, target_period, "S-2")

    assert seen.source == "marked_work"
    assert seen.answers
    assert all(a.question and a.objective_text for a in seen.answers)


async def test_a_learner_with_no_submission_has_no_answers(db: AsyncSession) -> None:
    workspace, target_period, _ = await _seed(db)

    seen = await LearnerAnswers().of(db, workspace, target_period, "S-2")

    assert seen.source == "none"
    assert seen.answers == []
