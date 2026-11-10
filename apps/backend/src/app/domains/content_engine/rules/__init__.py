"""The rules each content type's drafts are checked against, one tool of the app's MCP server each.

A rule reads ``{"draft": {"type", "sections"}, "source": {...} | None}`` and returns the faults it
finds, each naming its step; an empty list means the draft passes.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from .class_test.review import review as class_test_faults
from .lesson_note.review import review as lesson_note_faults
from .revision_note.review import review as revision_note_faults
from .slide_deck.review import review as slide_deck_faults

Rule = Callable[[Mapping[str, object]], list[str]]

#: Each rule by the name of the MCP tool a plugin lists to have its drafts checked with it.
RULES: Mapping[str, Rule] = {
    "check_slide_deck": slide_deck_faults,
    "check_lesson_note": lesson_note_faults,
    "check_revision_note": revision_note_faults,
    "check_class_test": class_test_faults,
}
