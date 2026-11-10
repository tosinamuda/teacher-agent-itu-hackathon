"""A context variant changes one field, and the wire says so.

The variant registry derives a named C1 from the frozen one, and the wire tap
records what a run would send. Together they let a diagnostic claim "the only
difference between these arms is field X" as a measurement rather than an
intention. These pin the three properties that claim rests on.
"""

from __future__ import annotations

import asyncio
import json

import pytest

from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES
from app.domains.experiments.review_pack_study.conditions.variants import (
    CONTEXT_VARIANTS,
    FROZEN_VARIANT,
    profiles_for_variant,
)
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.wire import NOT_ON_THE_WIRE, WireRequest, compare, render_arm

CASES = json.loads(EVAL_SET_PATH.read_text())["cases"]
PLANS = {c["lesson"]: SessionPlanView.model_validate(c["plan"]) for c in CASES}
ONE_LESSON = {"t3-w02": PLANS["t3-w02"]}
BARE_STEP = "step-t3w02-04"


def test_the_frozen_variant_is_the_frozen_conditions() -> None:
    for code, profile in profiles_for_variant(FROZEN_VARIANT).items():
        assert profile.context == H1_CONDITION_PROFILES[code].context
        assert profile.description == H1_CONDITION_PROFILES[code].description


@pytest.mark.parametrize("name", sorted(CONTEXT_VARIANTS))
def test_c0_is_the_same_c0_under_every_variant(name: str) -> None:
    assert profiles_for_variant(name)[ConditionCode.C0] == H1_CONDITION_PROFILES[ConditionCode.C0]


@pytest.mark.parametrize("name", sorted(set(CONTEXT_VARIANTS) - {FROZEN_VARIANT}))
def test_a_variant_changes_exactly_one_context_field_from_its_parent(name: str) -> None:
    parent = CONTEXT_VARIANTS[name].parent
    assert parent is not None
    base = profiles_for_variant(parent)[ConditionCode.C1].context.model_dump()
    varied = profiles_for_variant(name)[ConditionCode.C1].context.model_dump()
    changed = {k for k in base if base[k] != varied[k]}
    assert len(changed) == 1, changed


def test_a_variant_is_applied_to_the_whole_ladder_not_one_rung() -> None:
    varied = profiles_for_variant("v4-activities")
    for code in (ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        assert varied[code].context.include_teacher_student_activities is True


def test_an_unknown_variant_is_refused_by_name() -> None:
    with pytest.raises(ValueError, match="unknown context variant 'v9'"):
        profiles_for_variant("v9")


def test_the_frozen_profiles_are_not_mutated_by_deriving_from_them() -> None:
    before = {c: p.context.model_dump() for c, p in H1_CONDITION_PROFILES.items()}
    profiles_for_variant("v4-activities")
    assert {c: p.context.model_dump() for c, p in H1_CONDITION_PROFILES.items()} == before


def test_the_secret_never_enters_a_fingerprint() -> None:
    request = WireRequest(
        "m", [{"role": "user", "content": "x"}], {"api_key": "s3cret", "temperature": 0}
    )
    assert "api_key" in NOT_ON_THE_WIRE
    assert "s3cret" not in request.canonical()
    assert "s3cret" not in request.readable()
    assert "api_key" not in request.body()["kwargs"]


def test_the_fingerprint_covers_the_tools_the_adapter_puts_in_the_prompt() -> None:
    with_tools = WireRequest("m", [{"role": "user", "content": "[[ ## tools ## ]]\\n[...]"}], {})
    without = WireRequest("m", [{"role": "user", "content": "[[ ## tools ## ]]\\n[other]"}], {})
    assert with_tools.tools_in_prompt
    assert with_tools.digest() != without.digest()


_RENDERED: dict[str, tuple] = {}


@pytest.fixture
def both_arms() -> tuple:
    """Both arms rendered once per session, under the conftest's stand-in key.

    Function-scoped on purpose: the autouse fixture that installs the stand-in
    key is function-scoped, and a module-scoped fixture would build the LM
    before it runs.
    """
    if "arms" not in _RENDERED:
        conditions = (ConditionCode.C0, ConditionCode.C1)
        v3 = asyncio.run(render_arm("v3", plans=ONE_LESSON, conditions=conditions))
        v4 = asyncio.run(render_arm("v4-activities", plans=ONE_LESSON, conditions=conditions))
        _RENDERED["arms"] = (v3, v4)
    return _RENDERED["arms"]


@pytest.fixture
def bare_step_arms() -> tuple:
    """t3-w02 with its perimeter step's activities removed: every cohort step carries some."""
    if "bare" not in _RENDERED:
        plan = PLANS["t3-w02"]
        steps = [
            step.model_copy(update={"activities": []}) if step.step_id == BARE_STEP else step
            for step in plan.steps
        ]
        lesson = {"t3-w02": plan.model_copy(update={"steps": steps})}
        conditions = (ConditionCode.C1,)
        v3 = asyncio.run(render_arm("v3", plans=lesson, conditions=conditions))
        v4 = asyncio.run(render_arm("v4-activities", plans=lesson, conditions=conditions))
        _RENDERED["bare"] = (v3, v4)
    return _RENDERED["bare"]


def test_on_the_wire_c0_is_byte_identical_across_variants(both_arms: tuple) -> None:
    rows = compare(*both_arms)["units"]
    c0 = [r for r in rows if r["condition"] == "C0"]
    assert c0 and all(r["status"] == "identical" for r in c0)


def test_on_the_wire_the_variant_is_a_pure_insertion_of_its_one_field(both_arms: tuple) -> None:
    """One key added to one field, nothing removed and nothing else changed.

    Asserted structurally, on the adapter's own field blocks. A text diff cannot
    make this claim: the added key lands in the middle of the unit's JSON, so a
    prefix/suffix diff reports the shifted tail as removed and a character-level
    one invents alignments inside the JSON.
    """
    rows = compare(*both_arms)["units"]
    differing = [r for r in rows if r["condition"] == "C1" and r["status"] == "differs"]
    assert len(differing) == 3, "every C1 unit differs: the codebook gains the field's entry"
    for row in differing:
        payload = [x for x in row["diff"] if x["field"] == "unit_context"]
        instructions = [x for x in row["diff"] if x["field"].startswith("system")]
        assert instructions, "the condition must be told what the new field is"
        # No removal from the PAYLOAD. The instructions are a block of text that
        # gains an entry, so they show as replaced rather than appended; the data
        # is what must only ever grow.
        assert not any("removed" in x for x in payload), payload
        assert [x["key"] for x in payload] == ["activities"], payload


def test_a_unit_with_no_activities_gains_nothing_in_its_payload(bare_step_arms: tuple) -> None:
    """A step with no activities changes only in its codebook.

    It is not byte-identical: a condition is told about the fields it carries, so
    turning the field on changes what every one of its units is told even where the
    lesson has nothing to put in it.
    """
    rows = compare(*bare_step_arms)["units"]
    bare = next(r for r in rows if r["condition"] == "C1" and r["objective"] == "lo-t3w02-03")
    assert not [x for x in bare["diff"] if x["field"] == "unit_context"]
    assert [x for x in bare["diff"] if x["field"].startswith("system")]
