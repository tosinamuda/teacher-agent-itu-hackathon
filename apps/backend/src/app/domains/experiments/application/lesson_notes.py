"""Where each lesson's lesson note stands, as the experiment views read it."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LessonNoteState:
    """A plan version's newest lesson note, and whether the teacher has approved it."""

    artefact_id: str
    approved: bool


class LessonNotesReader(Protocol):
    """Each plan version's newest lesson note, read for many versions at once."""

    async def latest_lesson_notes(
        self, plan_version_ids: Sequence[str]
    ) -> dict[str, LessonNoteState]: ...
