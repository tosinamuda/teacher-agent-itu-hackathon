"""A concluded study's record is read-only."""

from __future__ import annotations


class ConcludedLessonError(Exception):
    """A write reached the record of a lesson whose study has concluded."""

    detail = "concluded_lesson_is_read_only"
