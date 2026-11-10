"""What one H1 experiment is handed before it starts."""

from __future__ import annotations

from dataclasses import dataclass

from ..conditions.study_design import StudyDesignConfig
from ..run import ExperimentRun, LessonUnderStudy


@dataclass(frozen=True)
class H1ExperimentInput:
    """One H1 execution: which run it is, the lesson it studies, the design it follows."""

    run: ExperimentRun
    lesson: LessonUnderStudy
    design: StudyDesignConfig
