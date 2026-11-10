"""Which expert content a revision note is grounded in."""

from __future__ import annotations

from enum import Enum


class ExpertSources(str, Enum):
    #: Each step's lesson note, and the plan's references for a step that has none: the rule
    #: the study's revision notes were generated under.
    LESSON_NOTE = "lesson-note"
    #: The plan's references (the textbook) only.
    TEXTBOOK = "textbook"
    #: Each step's lesson note together with the plan's references.
    BOTH = "both"
