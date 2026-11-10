"""Adjacent H1 conditions must differ in exactly one policy dimension.

The ablation only means something if C0->C1 moves the generation unit and the
step context, C1->C2 moves the textbook grounding, and C2->C3 moves nothing at
all except the validation policy. These tests diff the built requests
structurally (whole ``model_dump`` trees, reported by JSON path) rather than by
string containment, and pin that building one condition cannot disturb another.
"""

from __future__ import annotations

import os
import re

from condition_canaries import CANARY_CLASSES, request_probe
from condition_plan_inputs import build_request, h1_profiles, session_plans
from hypothesis import given, settings
from pydantic import BaseModel

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import (
    ConditionProfile,
    profile_for,
)
from app.shared.session_plan_view import SessionPlanView

_EXAMPLES = int(os.environ.get("LEAKAGE_EXAMPLES", "30"))
DIFFERENTIALS = settings(max_examples=_EXAMPLES, deadline=None, derandomize=_EXAMPLES <= 30)

_MISSING = object()

# The generation-unit change rewrites every unit, so C0->C1 is pinned on what
# it must NOT touch outside the unit list.
_UNIT_PATH = re.compile(r"^units(\[|$)")
_GROUNDING_PATH = re.compile(r"^units\[\d+\]\.(source_evidence|source_figures)")
_GROUNDING_POLICY_PATHS = frozenset(
    {"policy.require_source_refs", "policy.use_only_provided_sources", "policy.instruction_summary"}
)


def _profile(code: ConditionCode) -> ConditionProfile:
    return profile_for(Hypothesis.H1, code)


def _flatten(value: object, prefix: str = "") -> dict[str, object]:
    if isinstance(value, dict) and value:
        flat: dict[str, object] = {}
        for key, item in value.items():
            flat |= _flatten(item, f"{prefix}.{key}" if prefix else str(key))
        return flat
    if isinstance(value, list) and value:
        flat = {}
        for index, item in enumerate(value):
            flat |= _flatten(item, f"{prefix}[{index}]")
        return flat
    return {prefix: value}


def _changed_paths(left: object, right: object) -> set[str]:
    """Every JSON path whose value differs, was added, or was removed."""
    flat_left, flat_right = _flatten(left), _flatten(right)
    return {
        path
        for path in flat_left.keys() | flat_right.keys()
        if flat_left.get(path, _MISSING) != flat_right.get(path, _MISSING)
    }


def _body(request: ReviewPackRequest) -> dict:
    """The model-facing request, excluding its product execution policy."""
    return request.model_dump(exclude={"generation_policy"})


def _object_ids(value: object) -> set[int]:
    if isinstance(value, BaseModel):
        found = {id(value)}
        for name in type(value).model_fields:
            found |= _object_ids(getattr(value, name))
        return found
    if isinstance(value, (list, dict)):
        found = {id(value)}
        for item in value.values() if isinstance(value, dict) else value:
            found |= _object_ids(item)
        return found
    return set()


def _mutable_ids(request: ReviewPackRequest) -> set[int]:
    """Identity of every mutable node in a request, minus the shared profile.

    Condition profiles are frozen registry singletons and are deliberately
    shared; everything else is per-request state that later in-place section
    normalisation could otherwise mutate across conditions.
    """
    found = {id(request)}
    for name in type(request).model_fields:
        if name != "generation_policy":
            found |= _object_ids(getattr(request, name))
    return found


def _present_classes(request: ReviewPackRequest) -> set[str]:
    return {
        canary.name
        for canary in CANARY_CLASSES
        if canary.found_in(request_probe(request, canary.probe))
    }


@DIFFERENTIALS
@given(plan=session_plans())
def test_c0_to_c1_changes_only_the_plan_design_slices(
    plan: SessionPlanView,
) -> None:
    """The C0->C1 manipulation, stated as a diff.

    C1 adds the plan's instructional guidance and nothing else: the per-step
    units, and the lesson-level design slices her plan states — prior knowledge
    and the materials the lesson uses. Every other field is shared context both
    conditions receive, and the two arms are asked to write the same thing.
    """
    c0 = build_request(plan, _profile(ConditionCode.C0))
    c1 = build_request(plan, _profile(ConditionCode.C1))
    changed = _changed_paths(_body(c0), _body(c1))
    design = ("lesson_context.entry_behaviour", "lesson_context.instructional_materials")
    outside_units = {
        path for path in changed if not _UNIT_PATH.match(path) and not path.startswith(design)
    }
    assert outside_units == set(), sorted(outside_units)
    assert not c0.lesson_context.entry_behaviour and c1.lesson_context.entry_behaviour
    assert not c0.lesson_context.instructional_materials
    assert c1.lesson_context.instructional_materials
    # The design slices aside, the shared context must be identical — including
    # the instruction, so the two arms are given the same task.
    shared = {"entry_behaviour", "instructional_materials"}
    assert c0.lesson_context.model_dump(exclude=shared) == c1.lesson_context.model_dump(
        exclude=shared
    )
    assert c0.policy.instruction_summary == c1.policy.instruction_summary
    assert any(_UNIT_PATH.match(path) for path in changed), "the unit change went missing"


@DIFFERENTIALS
@given(plan=session_plans())
def test_c0_information_is_a_strict_subset_of_c1(plan: SessionPlanView) -> None:
    c0_profile, c1_profile = _profile(ConditionCode.C0), _profile(ConditionCode.C1)
    c0, c1 = build_request(plan, c0_profile), build_request(plan, c1_profile)
    for canary in CANARY_CLASSES:
        if canary.expected(c0_profile):
            assert canary.expected(c1_profile), f"C1 dropped {canary.name!r}"
    assert _present_classes(c0) < _present_classes(c1)
    assert c0.policy.model_dump(exclude={"instruction_summary"}) == c1.policy.model_dump(
        exclude={"instruction_summary"}
    )


@DIFFERENTIALS
@given(plan=session_plans())
def test_c1_to_c2_changes_only_the_grounding(plan: SessionPlanView) -> None:
    c1 = build_request(plan, _profile(ConditionCode.C1))
    c2 = build_request(plan, _profile(ConditionCode.C2))
    changed = _changed_paths(_body(c1), _body(c2))
    offenders = {
        path
        for path in changed
        if not _GROUNDING_PATH.match(path) and path not in _GROUNDING_POLICY_PATHS
    }
    assert not offenders, sorted(offenders)
    assert any(_GROUNDING_PATH.match(path) for path in changed), "the grounding change went missing"
    assert [unit.unit_id for unit in c1.units] == [unit.unit_id for unit in c2.units]
    assert [unit.step_content for unit in c1.units] == [unit.step_content for unit in c2.units]


@DIFFERENTIALS
@given(plan=session_plans())
def test_c2_to_c3_changes_nothing_but_the_validation_policy(plan: SessionPlanView) -> None:
    c2 = build_request(plan, _profile(ConditionCode.C2))
    c3 = build_request(plan, _profile(ConditionCode.C3))
    assert _body(c2) == _body(c3), sorted(_changed_paths(_body(c2), _body(c3)))
    profile_changed = _changed_paths(
        _profile(ConditionCode.C2).model_dump(),
        _profile(ConditionCode.C3).model_dump(),
    )
    assert {path.split(".")[0].split("[")[0] for path in profile_changed} == {
        "condition_code",
        "generated_by",
        "description",
        "validation",
    }


@DIFFERENTIALS
@given(plan=session_plans())
def test_build_order_never_changes_a_request(plan: SessionPlanView) -> None:
    """One builder, every condition: no condition may be contaminated by its siblings."""
    profiles = h1_profiles()
    builder = BaseReviewPackRequestBuilder()
    in_order = {
        profile.condition_code: build_request(plan, profile, builder=builder).model_dump_json()
        for profile in profiles
    }
    for start in range(len(profiles)):
        rotated = profiles[start:] + profiles[:start]
        shuffled = {
            profile.condition_code: build_request(plan, profile, builder=builder).model_dump_json()
            for profile in rotated
        }
        assert shuffled == in_order


@DIFFERENTIALS
@given(plan=session_plans())
def test_rebuilding_a_condition_is_byte_identical(plan: SessionPlanView) -> None:
    for profile in h1_profiles():
        first = build_request(plan, profile).model_dump_json()
        second = build_request(plan, profile).model_dump_json()
        assert first == second


@DIFFERENTIALS
@given(plan=session_plans())
def test_conditions_share_no_mutable_state(plan: SessionPlanView) -> None:
    """Section normalisation mutates blocks in place, so shared nodes would leak backwards."""
    requests = {profile.condition_code: build_request(plan, profile) for profile in h1_profiles()}
    seen: dict[int, ConditionCode] = {}
    for code, request in requests.items():
        for node in _mutable_ids(request):
            owner = seen.setdefault(node, code)
            assert owner == code, f"{code.value} shares a mutable node with {owner.value}"


@DIFFERENTIALS
@given(plan=session_plans())
def test_units_never_share_a_figure_block(plan: SessionPlanView) -> None:
    """``_append_grounded_figures`` rewrites a figure's objective id in place."""
    for profile in h1_profiles():
        seen: set[int] = set()
        for unit in build_request(plan, profile).units:
            for figure in unit.source_figures:
                assert id(figure) not in seen
                seen.add(id(figure))
