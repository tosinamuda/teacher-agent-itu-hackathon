"""A learner's lessons: the class test they sat for each, and where their revision note stands."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus

NoteStatus = Literal["to_review", "approved", "waiting_for_test", "not_made"]


@dataclass(frozen=True)
class LessonNote:
    artefact_id: str
    status: ArtefactReviewStatus


@dataclass(frozen=True)
class PlannedLesson:
    lesson_period_id: uuid.UUID
    title: str
    note: LessonNote | None


@dataclass(frozen=True)
class ClassTestTaken:
    lesson_period_id: uuid.UUID
    taken_at: datetime


def note_status(note: LessonNote | None, test_taken: bool) -> NoteStatus:
    """Where a learner's revision note for a lesson stands."""
    if note is not None:
        return "approved" if note.status == ArtefactReviewStatus.APPROVED else "to_review"
    return "not_made" if test_taken else "waiting_for_test"


def in_display_order(
    planned: list[PlannedLesson], tests: list[ClassTestTaken]
) -> list[PlannedLesson]:
    """Lessons with a test come first, newest test first; the rest keep the order taught."""
    taken_at = {test.lesson_period_id: test.taken_at for test in tests}
    sat = sorted(
        (lesson for lesson in planned if lesson.lesson_period_id in taken_at),
        key=lambda lesson: taken_at[lesson.lesson_period_id],
        reverse=True,
    )
    return [*sat, *(lesson for lesson in planned if lesson.lesson_period_id not in taken_at)]
