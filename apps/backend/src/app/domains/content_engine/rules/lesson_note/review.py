"""Every fault of a lesson note: each step's own, then what the steps say to each other."""

from __future__ import annotations

from collections.abc import Mapping

from .across_steps import Steps, repeated_questions
from .faults import step_faults
from .rounding_taught import rounding_taught


def _steps(payload: Mapping[str, object]) -> Steps:
    draft = payload.get("draft")
    sections = draft.get("sections") if isinstance(draft, dict) else None
    return [
        (str(section["unit_id"]), section["part"])
        for section in (sections if isinstance(sections, list) else [])
        if isinstance(section, dict) and isinstance(section.get("part"), dict)
    ]


def review(payload: Mapping[str, object]) -> list[str]:
    """The faults of the draft a payload holds; empty when the note passes."""
    steps = _steps(payload)
    return [
        *(f"{step}: {fault}" for step, part in steps for fault in step_faults(part)),
        *repeated_questions(steps),
        *rounding_taught(steps),
    ]
