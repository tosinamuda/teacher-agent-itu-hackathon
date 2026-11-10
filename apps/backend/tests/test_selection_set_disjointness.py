"""Nothing a harness is chosen on may have been seen by the endpoint it is measured against.

Selection tunes an instrument. Tuning it on the frozen eval set would make the H1a result a
measurement of a choice made using that same data, so disjointness is asserted rather than
intended — and asserted on content, not only on lesson names, because a renamed copy of a
frozen lesson would pass a name check.
"""

from __future__ import annotations

import json
import re

import pytest

from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.selection_set import (
    LESSONS,
    SCREENING_CONDITION,
    SELECTION_SET_PATH,
    freeze,
    frozen_eval_lessons,
)

FROZEN = json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))["cases"]
SELECTION = json.loads(SELECTION_SET_PATH.read_text(encoding="utf-8"))["cases"]
_WORD = re.compile(r"[a-z]{4,}")


def _notes(cases: list[dict]) -> str:
    return "\n".join(
        step.get("note") or ""
        for case in cases
        for step in case["plan"]["steps"]
        if step.get("note")
    )


def test_no_lesson_is_in_both_sets() -> None:
    assert {case["lesson"] for case in SELECTION} & frozen_eval_lessons() == set()


def test_no_plan_content_is_in_both_sets() -> None:
    """A renamed copy would pass a name check; the hash is what refuses one."""
    assert {case["plan_sha256"] for case in SELECTION} & {
        case["plan_sha256"] for case in FROZEN
    } == set()


def test_no_note_text_is_shared_between_the_sets() -> None:
    """The notes are what a grounded arm teaches from, so they carry the leak risk."""
    frozen_lines = {line.strip() for line in _notes(FROZEN).splitlines() if len(line.strip()) > 30}
    selection_lines = {
        line.strip() for line in _notes(SELECTION).splitlines() if len(line.strip()) > 30
    }

    assert frozen_lines & selection_lines == set()


def test_the_selection_set_covers_the_shapes_the_cohort_audit_found() -> None:
    """Built to span the real structural variation, not to be easy."""
    shapes = {}
    for case in SELECTION:
        steps = case["plan"]["steps"]
        core = [step for step in steps if step["step_kind"] == "core"]
        shapes[case["lesson"]] = (
            sum(1 for step in core for block in step["blocks"] if block.get("type") == "practice"),
            sum(1 for step in steps if step["step_kind"] == "evaluation"),
            any("tikzpicture" in (step.get("note") or "") for step in core),
        )

    assert shapes["sel-rich"][0] > 0, "no lesson carries practice blocks"
    assert shapes["sel-noprac"][0] == 0, "no lesson reproduces the missing-practice shape"
    assert shapes["sel-noeval"][1] == 0, "no lesson reproduces t3-w06's missing evaluation step"
    assert shapes["sel-drawn"][2], "no lesson carries a drawing inside the note"


def test_screening_happens_where_the_metric_can_see_the_note() -> None:
    """Recall is scored against the note, and C0 and C1 never receive it."""
    assert SCREENING_CONDITION.value in {"C2", "C3"}


def test_the_committed_set_matches_the_declaration() -> None:
    expected = json.dumps(freeze(), indent=2) + "\n"

    assert SELECTION_SET_PATH.read_text(encoding="utf-8") == expected, (
        "the selection set is stale — regenerate with "
        "`uv run python -m experiments.h1_condition_eval.selection_set`"
    )


@pytest.mark.parametrize("key", sorted(LESSONS))
def test_every_selection_lesson_carries_a_note_to_ground_from(key: str) -> None:
    """A grounded screen needs evidence; a lesson with no note would screen nothing."""
    core = [step for step in LESSONS[key]["steps"] if step["step_kind"] == "core"]

    assert core, f"{key} has no core step"
    assert all(step.get("note") for step in core), f"{key} has a core step with no note"
