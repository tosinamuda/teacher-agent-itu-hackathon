"""A second reader for a finished draft: it checks each part against the brief it was written to.

A writer that wrote a wrong step reads its own step as right; a reader that must work every
calculation and construction again, and read the part against each requirement and skill rule
of the brief, catches what the writer did not. The brief is the type's own, so the rules the
reader enforces belong to the plugin, not to the engine. What it finds goes back to the writer
to correct, like any issue.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence

import dspy

from app.shared.json_types import JsonObject

#: What a checker reads about the lesson besides the unit itself.
_LESSON_FACTS = ("subject", "grade", "topic", "subtopic")


class CheckerStoppedError(RuntimeError):
    """The checker ended without an answer its schema allows."""


class CheckPart(dspy.Signature):
    """Check one part of a draft against the brief, as the teacher who reads it would.

    The brief holds the requirements the part must meet and the skills it is written with.
    First, work every calculation, every answer and every construction step through yourself,
    and read every drawing's TikZ against its caption. List each real error: a false
    statement, a wrong line of working or answer, a construction step that cannot work as
    written, a drawing that does not show what its caption says, or a reference to a diagram,
    figure or picture ("as shown") that the part does not draw.
    Then read the part once for each requirement of the brief and each rule of a skill the
    brief gives, where it applies, wording and layout rules included, and list each place the
    part breaks one: quote the requirement or rule, say where in the part it is broken and
    what is right instead. Judge a part only by the brief's own requirements and rules, and
    never by a preference of your own. Return an empty list when the part has no errors and
    breaks no requirement or rule.
    """

    brief: dict[str, object] = dspy.InputField(
        desc="What the part is for and must meet, with the skills it is written with."
    )
    unit: dict[str, object] = dspy.InputField(
        desc="The unit the part covers, as the lesson has it."
    )
    part: dict[str, object] = dspy.InputField(desc="The part to check.")
    errors: list[str] = dspy.OutputField(
        desc="Each real error or broken requirement or rule, where it is, and the correction."
    )


def unit_context(
    lesson: JsonObject, unit: JsonObject, fields: Sequence[str] = ()
) -> dict[str, object]:
    """The unit as a checker reads it: the lesson's facts, and the plan step it covers.

    It also names the fields the unit's part holds, so the checker does not ask a part for what
    another unit's part holds.
    """
    steps = lesson.get("steps")
    step = (
        next(
            (s for s in steps if isinstance(s, dict) and s.get("step_id") == unit.get("unit_id")),
            None,
        )
        if isinstance(steps, list)
        else None
    )
    facts = {name: lesson.get(name) for name in _LESSON_FACTS if lesson.get(name)}
    held = {"fields_this_part_holds": [*fields]} if fields else {}
    return {**facts, "unit": unit, "plan_step": step, **held}


class PartChecker:
    def __init__(self, lm: dspy.BaseLM) -> None:
        self._check = dspy.ChainOfThought(CheckPart)
        self._lm = lm

    async def errors(
        self, brief: JsonObject, unit: dict[str, object], part: JsonObject
    ) -> list[str]:
        """The part's real errors; empty when it has none."""

        def check() -> list[str]:
            with dspy.context(lm=self._lm):
                result = self._check(brief=brief, unit=unit, part=part)
            return [
                str(error) for error in getattr(result, "errors", []) or [] if str(error).strip()
            ]

        return await asyncio.to_thread(check)
