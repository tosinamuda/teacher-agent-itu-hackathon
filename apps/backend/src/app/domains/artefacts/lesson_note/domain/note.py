"""A lesson note: the subject content a teacher teaches, one markdown section per plan step.

A teacher writes one, a study's record carries one, or the app drafts one for the teacher to
check. All three are the same record; where it came from is its origin. Markdown is the
form a note is read in, by a teacher and by generation alike.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.shared.llm_markup import reader_ready

#: Where a lesson note came from: written by the teacher, carried by a study's record, drafted by
#: the app, or copied from the note of another plan. Only an approved note is ever read as the
#: lesson's note.
Origin = Literal["teacher", "study_record", "generated", "reused"]


class NoteSection(BaseModel):
    """The note for one plan step."""

    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1, description="The note, as markdown.")


class LessonNote(BaseModel):
    """The stored manifest of a lesson note."""

    model_config = ConfigDict(extra="forbid")

    artefact_type: Literal["lesson_note"] = "lesson_note"
    plan_version_id: str
    sections: list[NoteSection] = Field(default_factory=list)


class WorkedExample(BaseModel):
    """A problem with its solution worked through."""

    model_config = ConfigDict(extra="forbid")

    problem: str = Field(..., min_length=1)
    solution: str = Field(..., min_length=1, description="The working, step by step.")


class ClassQuestion(BaseModel):
    """A question for the teacher to ask, with the answer the class should reach."""

    model_config = ConfigDict(extra="forbid")

    question: str = Field(..., min_length=1)
    expected_answer: str = Field(..., min_length=1)


#: A list marker the model wrote into a point that is set as a list item already.
_BULLET_RE = re.compile(r"^\s*[-*•–]\s+")
_NUMBER_RE = re.compile(r"^\s*(\d+)([.)])\s+")


def _as_point(point: str) -> str:
    """A teaching point as one bullet: its own bullet dropped, its own number kept as text."""
    return _NUMBER_RE.sub(r"\1\\\2 ", _BULLET_RE.sub("", point, count=1), count=1)


class NoteStepDraft(BaseModel):
    """One step's note as the drafting model writes it, before it becomes markdown."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1)
    teaching_points: list[str] = Field(
        ..., min_length=1, description="What to explain, in the order to explain it."
    )
    worked_examples: list[WorkedExample] = Field(default_factory=list)
    class_questions: list[ClassQuestion] = Field(default_factory=list)
    board_summary: str = Field(..., min_length=1, description="What stays on the board.")

    def as_markdown(self) -> str:
        """The note in the conventions a teacher's own note uses: headed parts, marked solutions.

        A question and its answer may each be a textbook exercise running to several
        paragraphs of working, so each stands as blocks of its own rather than in a list.
        """
        points = "\n".join(f"- {_as_point(point)}" for point in self.teaching_points)
        parts = [f"#### {self.title}", points]
        for number, example in enumerate(self.worked_examples, start=1):
            parts.append(
                f"#### Example {number}.\n\n{example.problem}\n\n**Solution**\n\n{example.solution}"
            )
        if self.class_questions:
            parts.append("#### Questions for the class")
            for number, item in enumerate(self.class_questions, start=1):
                parts.append(
                    f"**Question {number}.**\n\n{item.question}\n\n"
                    f"*Expected answer:*\n\n{item.expected_answer}"
                )
        parts.append(f"#### On the board\n\n{self.board_summary}")
        return reader_ready("\n\n".join(parts))
