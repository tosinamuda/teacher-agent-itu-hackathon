"""The plan as a revision note is generated from it: each step carrying its lesson note.

The lesson plan and the lesson note are separate records. Generation reads them together,
the note of a step as that step's ``note``, which is how the study's generator read them.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def with_lesson_note(
    session_plan: Mapping[str, Any], sections: Mapping[str, str]
) -> dict[str, Any]:
    """The plan with each step's lesson note, where the note has a section for that step."""
    steps = [
        {**step, "note": sections[step["step_id"]]}
        if step.get("step_id") in sections
        else dict(step)
        for step in session_plan.get("steps") or []
    ]
    return {**session_plan, "steps": steps}
