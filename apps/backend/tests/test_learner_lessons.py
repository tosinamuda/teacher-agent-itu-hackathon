import uuid
from datetime import datetime

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.teaching.domain.learner_lessons import (
    ClassTestTaken,
    LessonNote,
    PlannedLesson,
    in_display_order,
    note_status,
)


def test_a_note_is_to_review_or_approved_as_the_teacher_left_it() -> None:
    pending = LessonNote("A-1", ArtefactReviewStatus.PENDING)
    approved = LessonNote("A-2", ArtefactReviewStatus.APPROVED)

    assert note_status(pending, test_taken=True) == "to_review"
    assert note_status(approved, test_taken=True) == "approved"


def test_without_a_note_it_waits_for_the_test_or_has_not_been_made() -> None:
    assert note_status(None, test_taken=False) == "waiting_for_test"
    assert note_status(None, test_taken=True) == "not_made"


def test_lessons_with_a_test_come_first_newest_first_then_the_rest_as_taught() -> None:
    first, second, third, fourth = (uuid.uuid4() for _ in range(4))
    planned = [
        PlannedLesson(lesson, name, None)
        for lesson, name in zip(
            (first, second, third, fourth), ("one", "two", "three", "four"), strict=True
        )
    ]
    tests = [
        ClassTestTaken(first, datetime(2026, 11, 1)),
        ClassTestTaken(third, datetime(2026, 11, 5)),
    ]

    assert [lesson.title for lesson in in_display_order(planned, tests)] == [
        "three",
        "one",
        "two",
        "four",
    ]
