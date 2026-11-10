"""A lesson note drafted from the plan alone: markdown per step, pending, revised, approved."""

from __future__ import annotations

import asyncio

import dspy
import pytest
from sqlalchemy import text

from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.lesson_note_executor import (
    LessonNoteRevisionExecutor,
)
from app.domains.artefact_revision.application.service import ArtefactRevisionService
from app.domains.artefacts.core.application.service import ArtefactApplicationError
from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.wiring import build_lifecycle_manager
from app.domains.artefacts.lesson_note.application.draft import (
    DraftLessonNote,
    NoteLesson,
    NoteStepInput,
    note_inputs,
)
from app.domains.artefacts.lesson_note.application.errors import UnreadableReplyError
from app.domains.artefacts.lesson_note.application.service import LessonNoteService
from app.domains.artefacts.lesson_note.domain.note import (
    ClassQuestion,
    NoteSection,
    NoteStepDraft,
    WorkedExample,
)
from app.domains.artefacts.lesson_note.infrastructure.dspy.write_note_step import (
    WriteNoteStep,
)
from app.domains.artefacts.lesson_note.infrastructure.repository import SqlAlchemyLessonNotes
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.shared.session_plan_view import SessionPlanView
from tests.log_tags import active_log_tags

TEACHERS_NOTE = "Her own words: BODMAS means brackets first."
SESSION_PLAN = {
    "subject": "Mathematics",
    "grade": "JSS1",
    "topic": "Order of operations",
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lop01", "objective_text": "Evaluate expressions with brackets"},
        {"lesson_objective_id": "lop02", "objective_text": "Multiply before adding"},
    ],
    "steps": [
        {
            "step_id": "s1",
            "step_kind": "core",
            "lesson_objective_id": "lop01",
            "title": "Brackets",
            "content": "Work inside brackets first.",
            "note": TEACHERS_NOTE,
        },
        {
            "step_id": "s2",
            "step_kind": "core",
            "lesson_objective_id": "lop02",
            "title": "Multiplication",
            "content": "Multiply before adding.",
        },
    ],
}


def _part(title: str) -> NoteStepDraft:
    return NoteStepDraft(
        title=title,
        teaching_points=[f"explain {title}"],
        worked_examples=[WorkedExample(problem="2 + 3 × 4", solution="3 × 4 = 12; 2 + 12 = 14")],
        board_summary=f"{title} summary",
    )


class _Writer:
    def __init__(self) -> None:
        self.calls: list[tuple[ArtefactSpec, NoteStepInput]] = []
        self.tags: list[dict[str, object]] = []

    async def write(
        self, *, brief: ArtefactSpec, lesson: NoteLesson, step: NoteStepInput, draw: int = 0
    ) -> NoteStepDraft:
        self.calls.append((brief, step))
        self.tags.append(active_log_tags())
        return _part(step.title)


class _Reviser:
    def __init__(self, reorder: bool = False) -> None:
        self.reorder = reorder
        self.tags: list[dict[str, object]] = []

    async def revise(
        self,
        *,
        brief: ArtefactSpec,
        current_sections: list[NoteSection],
        highlighted_section: str,
        instruction: str,
    ) -> tuple[list[NoteSection], str]:
        self.tags.append(active_log_tags())
        revised = list(current_sections)
        revised[0] = revised[0].model_copy(update={"body": f"{revised[0].body}\n\n{instruction}"})
        return (revised[::-1] if self.reorder else revised), "Added the instruction to step 1."


LESSON_NOTE = seed_specification(ArtefactType.LESSON_NOTE.value)


def test_the_lesson_note_is_a_seeded_class_level_kind() -> None:
    assert LESSON_NOTE.levels == frozenset({ArtefactScope.CLASS_LEVEL})


def test_the_writer_is_given_plan_fields_and_never_a_note_already_there() -> None:
    _, steps = note_inputs(SessionPlanView.model_validate(SESSION_PLAN))

    assert [step.step_id for step in steps] == ["s1", "s2"]
    assert steps[0].objective_text == "Evaluate expressions with brackets"
    assert all(TEACHERS_NOTE not in step.model_dump_json() for step in steps)


def test_one_markdown_section_per_step_is_written_against_the_registered_brief() -> None:
    writer = _Writer()
    note = asyncio.run(
        DraftLessonNote(writer).draft(
            plan=SessionPlanView.model_validate(SESSION_PLAN),
            plan_version_id="LPV-N1",
            specification=LESSON_NOTE,
        )
    )

    expected = LESSON_NOTE.brief("a junior secondary student aged about 11-13")
    assert [brief for brief, _ in writer.calls] == [expected, expected]
    assert [(section.step_id, section.body) for section in note.sections] == [
        ("s1", _part("Brackets").as_markdown()),
        ("s2", _part("Multiplication").as_markdown()),
    ]
    assert writer.tags == 2 * [
        {"kind": "lesson_note", "correlation_id": "LPV-N1", "plan_version_id": "LPV-N1"}
    ]


def test_a_drafted_section_reads_like_a_teachers_note() -> None:
    """Headed parts and marked solutions: the conventions the study's teacher wrote in."""
    part = _part("Brackets").model_copy(
        update={"class_questions": [ClassQuestion(question="(2 + 3) × 4?", expected_answer="20")]}
    )

    assert part.as_markdown() == (
        "#### Brackets\n\n- explain Brackets\n\n"
        "#### Example 1.\n\n2 + 3 × 4\n\n**Solution**\n\n3 × 4 = 12; 2 + 12 = 14\n\n"
        "#### Questions for the class\n\n"
        "**Question 1.**\n\n(2 + 3) × 4?\n\n*Expected answer:*\n\n20\n\n"
        "#### On the board\n\nBrackets summary"
    )


def test_the_rendered_writer_prompt_carries_every_requirement() -> None:
    lesson, steps = note_inputs(SessionPlanView.model_validate(SESSION_PLAN))
    messages = dspy.ChatAdapter().format(
        dspy.ChainOfThought(WriteNoteStep).predict.signature,
        demos=[],
        inputs={
            "artefact_spec": LESSON_NOTE.brief("a junior secondary student"),
            "lesson": lesson,
            "step": steps[0],
        },
    )
    user = messages[-1]["content"]

    for requirement in LESSON_NOTE.requirements:
        assert requirement in user
    assert TEACHERS_NOTE not in user


async def _seed_plan(db, version_id: str) -> None:  # type: ignore[no-untyped-def]
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(
        PlanVersion(
            version_id=version_id,
            plan_id=f"P-{version_id}",
            source_type="experiment_manual",
            session_plan=SESSION_PLAN,
            status=PlanVersionStatus.DRAFT,
        )
    )
    await db.flush()


@pytest.mark.asyncio
async def test_a_drafted_note_is_stored_pending_revised_in_place_and_approved(db) -> None:
    await _seed_plan(db, "LPV-N2")
    notes = SqlAlchemyLessonNotes()
    service = LessonNoteService(notes, DraftLessonNote(_Writer()))

    created = await service.draft(db=db, plan_version_id="LPV-N2")
    note_id = created.artefact_id
    assert created.artefact_type == "lesson_note"
    assert created.review_status == ArtefactReviewStatus.PENDING
    assert created.artefact_refs == {
        "origin": "generated",
        "specification": {"kind": "lesson_note", "revision": 1},
    }
    assert (await service.latest(db=db, plan_version_id="LPV-N2")).artefact_id == note_id

    executor = LessonNoteRevisionExecutor(notes, _Reviser())
    outcome = await executor.revise(
        db=db,
        subject_id=note_id,
        thread_id="T-1",
        instruction="Put the rule in a box.",
        highlight=None,
        conversation_summary="",
    )
    await db.commit()
    revised = await notes.get(db, note_id)
    assert outcome.change_summary == "Added the instruction to step 1."
    assert revised.version == 2
    assert revised.manifest["sections"][0]["step_id"] == "s1"
    assert revised.manifest["sections"][0]["body"].endswith("Put the rule in a box.")

    manager = build_lifecycle_manager()
    approved = await manager.approve_artefact(
        db=db, artefact_id=note_id, reviewed_by="Teacher", expected_version=2
    )
    assert approved.review_status == ArtefactReviewStatus.APPROVED
    assert approved.version == 2
    # A second approval of the same text is refused. Last, because the refusal rolls the
    # session back.
    with pytest.raises(ArtefactApplicationError) as stale:
        await manager.approve_artefact(
            db=db, artefact_id=note_id, reviewed_by="Teacher", expected_version=2
        )
    assert stale.value.status_code == 409


@pytest.mark.asyncio
async def test_a_revision_turn_s_model_calls_are_tagged_with_its_thread(db) -> None:
    await _seed_plan(db, "LPV-N5")
    notes = SqlAlchemyLessonNotes()
    created = await LessonNoteService(notes, DraftLessonNote(_Writer())).draft(
        db=db, plan_version_id="LPV-N5"
    )
    reviser = _Reviser()
    service = ArtefactRevisionService((LessonNoteRevisionExecutor(notes, reviser),))
    thread = await service.get_or_create_thread(
        db=db, artefact_type="lesson_note", subject_id=created.artefact_id, created_by="T"
    )

    await service.submit_turn(
        db=db, thread_id=thread.revision_thread_id, instruction="Box it.", highlight=None
    )

    assert reviser.tags == [
        {
            "kind": "lesson_note_revision",
            "correlation_id": thread.revision_thread_id,
            "subject_id": created.artefact_id,
        }
    ]


@pytest.mark.asyncio
async def test_a_revision_that_moves_the_notes_sections_is_refused(db) -> None:
    await _seed_plan(db, "LPV-N4")
    notes = SqlAlchemyLessonNotes()
    created = await LessonNoteService(notes, DraftLessonNote(_Writer())).draft(
        db=db, plan_version_id="LPV-N4"
    )

    with pytest.raises(ValueError, match="revision_changed_the_note_s_sections"):
        await LessonNoteRevisionExecutor(notes, _Reviser(reorder=True)).revise(
            db=db,
            subject_id=created.artefact_id,
            thread_id="T-3",
            instruction="Swap them.",
            highlight=None,
            conversation_summary="",
        )


class _UnreadableReviser:
    async def revise(self, **_: object) -> tuple[list[NoteSection], str]:
        raise UnreadableReplyError("the reply was not readable")


@pytest.mark.asyncio
async def test_a_reply_the_model_gets_wrong_twice_is_a_502_not_a_crash(db) -> None:
    await _seed_plan(db, "LPV-N6")
    notes = SqlAlchemyLessonNotes()
    created = await LessonNoteService(notes, DraftLessonNote(_Writer())).draft(
        db=db, plan_version_id="LPV-N6"
    )

    with pytest.raises(ArtefactRevisionError) as refused:
        await LessonNoteRevisionExecutor(notes, _UnreadableReviser()).revise(
            db=db,
            subject_id=created.artefact_id,
            thread_id="T-4",
            instruction="Add an example.",
            highlight=None,
            conversation_summary="",
        )

    assert (refused.value.status_code, refused.value.detail) == (
        502,
        "the_model_reply_could_not_be_read",
    )


@pytest.mark.asyncio
async def test_the_executor_refuses_an_artefact_of_another_kind(db) -> None:
    executor = LessonNoteRevisionExecutor(SqlAlchemyLessonNotes(), _Reviser())

    assert await executor.current_artefact(db=db, subject_id="ART-NOT-A-NOTE") == (None, None)
    with pytest.raises(LookupError):
        await executor.revise(
            db=db,
            subject_id="ART-NOT-A-NOTE",
            thread_id="T-2",
            instruction="x",
            highlight=None,
            conversation_summary="",
        )


@pytest.mark.asyncio
async def test_the_pack_executor_does_not_read_a_note_as_a_pack(db) -> None:
    from app.domains.artefact_revision.application.review_pack_executor import (
        ReviewPackRevisionExecutor,
    )
    from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository

    await _seed_plan(db, "LPV-N3")
    created = await LessonNoteService(SqlAlchemyLessonNotes(), DraftLessonNote(_Writer())).draft(
        db=db, plan_version_id="LPV-N3"
    )
    pack_executor = ReviewPackRevisionExecutor(ArtefactRepository(), reviser=object())  # type: ignore[arg-type]

    assert await pack_executor.current_artefact(db=db, subject_id=created.artefact_id) == (
        None,
        None,
    )
