"""The first page of every set, in the shape of the worksheet raters have seen before.

Institution band, the title, a paragraph that frames the task, the lesson reference as
a key–value table, the lesson objectives, and — for Part 2 — the learner's evidence,
objective by objective. What the rater does with all this is on the next page.
"""

from __future__ import annotations

from typing import Any

from app.config import CONFIG

from . import reference
from .forms import key_value_table, objectives_table
from .layout import RULE

SET_HEADING = "Evaluation Set"
TITLE = "Revision Material Evaluation Worksheet"


def cover(
    *,
    external_id: str,
    part_title: str,
    rater_number: int,
    plan: dict[str, Any],
    welcome: str,
    contents: list[str],
    extra: list[str] = (),
) -> list[str]:
    lines = [
        f"**{CONFIG.institution_name.upper()}**",
        "",
        CONFIG.study_title,
        "",
        RULE,
        "",
        f"# {TITLE}",
        "",
        f"**{part_title}** · {SET_HEADING} {external_id} · Rater {rater_number}",
        "",
        welcome,
        "",
        "### Lesson reference",
        "",
        *key_value_table(reference.lesson_reference_rows(plan)),
        "### Lesson objectives",
        "",
        *objectives_table([text for _, text in reference.objectives(plan)]),
        *extra,
        "**In this set, in order.** " + " · ".join(contents),
        "",
        "**Date completed:** ____________________",
        "",
    ]
    return lines
