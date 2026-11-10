"""Draft a lesson note from an approved plan: one section per plan step, written concurrently.

The draft reads the plan and nothing else, so it cannot restate a note the teacher wrote. It
is stored with the origin "generated" and stays pending: only the teacher's approval makes it
the lesson's note, and only an approved note is ever read as one.
"""

from __future__ import annotations

import asyncio
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.core.domain.specification import ArtefactSpec, ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.lesson_note.domain.note import (
    ClassQuestion,
    LessonNote,
    NoteSection,
    NoteStepDraft,
)
from app.domains.generation_log.application.recorder import log_context
from app.shared.json_types import JsonObject
from app.shared.note_text import corrects_itself, without_record_ids
from app.shared.readers import reader_for
from app.shared.session_plan_view import SessionPlanView


class NoteLesson(BaseModel):
    """What the whole lesson tells every step's writer."""

    model_config = ConfigDict(extra="forbid")

    subject: str
    grade: str
    topic: str
    title: str
    entry_behaviour: list[str]
    instructional_materials: list[str]


class NoteStepInput(BaseModel):
    """One plan step, as the writer is given it."""

    model_config = ConfigDict(extra="forbid")

    step_id: str
    step_kind: str
    lesson_objective_id: str | None
    objective_text: str
    title: str
    content: str
    activities: list[JsonObject]
    questions: list[ClassQuestion] = Field(
        default_factory=list,
        description="The questions the plan itself sets in this step, with their answers.",
    )
    blocks: list[JsonObject] = Field(
        default_factory=list,
        description=(
            "The plan's own teaching for this step: explanations, worked examples with their "
            "working and figures, and practice. The note builds on these, never against them."
        ),
    )


class NoteStepWriter(Protocol):
    """Writes one step's note."""

    async def write(
        self, *, brief: ArtefactSpec, lesson: NoteLesson, step: NoteStepInput, draw: int = 0
    ) -> NoteStepDraft:
        """One draw of the step's note; draw 0 is the cached one, each later a fresh sample."""
        ...


def _questions(blocks: list[JsonObject]) -> list[ClassQuestion]:
    return [
        ClassQuestion(question=str(block["question"]), expected_answer=str(block["answer"]))
        for block in blocks
        if block.get("type") == "practice" and block.get("question") and block.get("answer")
    ]


def _teaching(block: JsonObject) -> JsonObject:
    """A plan block as a writer reads it: its teaching, without IDs or source bookkeeping."""
    return {
        name: value
        for name, value in block.items()
        if name not in ("id", "source_refs", "lesson_objective_id")
    }


def note_inputs(plan: SessionPlanView) -> tuple[NoteLesson, list[NoteStepInput]]:
    """The lesson and its steps in plan order, reading plan fields only."""
    objectives = {
        objective.lesson_objective_id: objective.objective_text or ""
        for objective in plan.lesson_plan_objectives
    }
    lesson = NoteLesson(
        subject=plan.subject or "",
        grade=plan.grade or "",
        topic=plan.topic or plan.subtopic or "",
        title=plan.title or plan.topic or "",
        entry_behaviour=list(plan.entry_behaviour),
        instructional_materials=list(plan.instructional_materials),
    )
    steps = [
        NoteStepInput(
            step_id=step.step_id,
            step_kind=step.step_kind,
            lesson_objective_id=step.lesson_objective_id,
            objective_text=objectives.get(step.lesson_objective_id or "", ""),
            title=step.title or "",
            content=step.content or "",
            activities=list(step.activities),
            questions=_questions(step.blocks),
            blocks=[_teaching(block) for block in step.blocks],
        )
        for step in plan.steps
    ]
    return lesson, steps


#: How many times a step's note is drawn when it leaves a second thought in the text.
_DRAWS = 3


class DraftLessonNote:
    """Write every step's note against the registered brief and assemble the manifest."""

    def __init__(self, writer: NoteStepWriter) -> None:
        self._writer = writer

    async def draft(
        self,
        *,
        plan: SessionPlanView,
        plan_version_id: str,
        specification: ContentSpecification,
    ) -> LessonNote:
        lesson, steps = note_inputs(plan)
        if not steps:
            raise ValueError("plan_has_no_steps")
        if specification.kind != ArtefactType.LESSON_NOTE.value:
            raise ValueError(f"not_a_lesson_note_specification:{specification.kind}")
        brief = specification.brief(reader_for(lesson.grade))
        with log_context(
            kind="lesson_note", correlation_id=plan_version_id, plan_version_id=plan_version_id
        ):
            bodies = await asyncio.gather(*(self._body(brief, lesson, step) for step in steps))
        return LessonNote(
            plan_version_id=plan_version_id,
            sections=[
                NoteSection(step_id=step.step_id, body=body)
                for step, body in zip(steps, bodies, strict=True)
            ],
        )

    async def _body(self, brief: ArtefactSpec, lesson: NoteLesson, step: NoteStepInput) -> str:
        """The step's note without the plan's record ids, drawn again while it corrects itself."""
        body = ""
        for draw in range(_DRAWS):
            part = await self._writer.write(brief=brief, lesson=lesson, step=step, draw=draw)
            body = without_record_ids(part.as_markdown())
            if not corrects_itself(body):
                break
        return body
