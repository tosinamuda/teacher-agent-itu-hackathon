"""No condition may receive plan content its ``ConditionProfile`` does not allow.

Canary-stamped plans (``condition_plan_inputs``) go through the REAL request
builder and then the REAL rendered prompt, and are judged against the leak map
(``condition_canaries``). A pydantic schema is not proof of what the model
sees, so the load-bearing assertions run against ``dspy.ChatAdapter().format``
output — what ``generation.py`` hands the LM.

Every expectation is derived from the profile object, so a profile edit moves
the expectations with it and an unmapped policy field fails outright.
"""

from __future__ import annotations

import os

import dspy
import pytest
from condition_canaries import (
    CANARY_CLASSES,
    STEP_PROSE_GATES,
    CanaryClass,
    Probe,
    assert_only_allowed,
    prompt_probes,
    request_probe,
)
from condition_plan_inputs import (
    EDGE_PROFILES,
    all_profiles,
    build_request,
    condition_profiles,
    example_plan,
    h1_profiles,
    session_plans,
)
from hypothesis import given, settings

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    unit_for_personalisation_repair,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.personalise_section import (  # noqa: E501
    SectionPersonalisation,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.repair_section import (  # noqa: E501
    RepairSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    shared_inputs,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import (
    ConditionProfile,
    ContextPolicy,
    profile_for,
)
from app.shared.session_plan_view import SessionPlanView

# Deterministic in CI: a fixed seed, and no per-example deadline (a cold import
# of the dspy adapter would otherwise flake the first example). A fuzz campaign
# is the same properties searched harder — LEAKAGE_EXAMPLES scales the budget and
# drops the fixed seed, so a long run explores instead of repeating.
_EXAMPLES = int(os.environ.get("LEAKAGE_EXAMPLES", "50"))
_DEEP = _EXAMPLES > 50
LEAKAGE = settings(max_examples=_EXAMPLES, deadline=None, derandomize=not _DEEP)
PROMPTS = settings(LEAKAGE, max_examples=max(_EXAMPLES // 2, 20))

# Plan slices no condition can carry, whatever its profile declares: the
# builder has no source for them.
ALWAYS_ABSENT = frozenset(
    {
        # No registered condition receives these verbatim slices. The step-prose
        # ones are withheld by design: the title paraphrases the objective, the
        # content duplicates the activities, instructional_type is a lossy parse
        # of the note, the activity prose is who-did-what in the room, and the
        # per-step timings were the derivation's rather than the teacher's.
        "step_title",
        "step_content",
        # The drawing an assessment question needs. No frozen condition carries it
        # — `v6-assessment-figures` does, and that is a variant, not a condition.
        "assessment_figures",
        "step_structure",
        "step_timing",
        "teacher_activities",
        "student_activities",
        # Derived values, not the teacher's words — nothing verbatim to detect.
        "lesson_sequence",
        "instructional_events",
        # Plan content no condition's request carries at all.
        "task_answers",
        "block_asides",
        "non_core_steps",
        "plan_asides",
    }
)

# Context gates the builder honours — synthetic profiles prove it — that no
# registered condition turns on, each with the reason it stays off. Her step
# prose is withheld by design; what a step TAUGHT travels as her note instead.
UNUSED_GATES = {
    "include_step_title": "her step title paraphrases the objective the unit already carries",
    "include_step_content": "her step content duplicates the activities and the note",
    "include_lesson_step_structure": "instructional_type is a lossy parse of the note",
    "include_teacher_student_activities": "who did what in the room, not teaching a learner reads",
    "include_assessment_figures": (
        "carries a drawing with the question that needs it; the v6-assessment-figures "
        "variant turns it on, the frozen conditions do not"
    ),
}

P1_PROFILE = profile_for(Hypothesis.H2, ConditionCode.P1)


class _ExplodingLM(dspy.BaseLM):
    """An LM that fails the test if anything tries to call it."""

    def __call__(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("prompt rendering must not reach an LM")

    async def acall(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("prompt rendering must not reach an LM")


_OFFLINE_GUARD = _ExplodingLM(model="offline-render-guard")


def _render(signature: type[dspy.Signature], inputs: dict) -> list[dict]:
    # Rendering runs with an LM that raises on any call — and other modules
    # configure dspy globally at import — so a render that returns is proof the
    # prompt was built without reaching a provider.
    with dspy.settings.context(lm=_OFFLINE_GUARD):
        return dspy.ChatAdapter().format(signature, demos=[], inputs=inputs)


def _prompt_probes(signature: type[dspy.Signature], inputs: dict) -> dict[Probe, str]:
    return prompt_probes([str(message["content"]) for message in _render(signature, inputs)])


def _generate_inputs(request: ReviewPackRequest, unit: SectionGenerationUnit) -> dict:
    """What the generator passes — by calling the same mapper it does.

    Assembling this by hand is how a prompt check reads a prompt no run
    produces. It drifted exactly that way once already: this helper claimed to
    mirror the call while passing the raw models the generator prunes, and
    omitting artefact_spec entirely.
    """
    return dict(shared_inputs(request=request, unit=unit))


def _neutral_section(objective_id: str) -> ReviewPackSection:
    """A section carrying no canary, so only the unit can make one appear."""
    return ReviewPackSection(
        section_id=f"sec-{objective_id}",
        title="Working with the objective",
        lesson_objective_id=objective_id,
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="Multiply the two side lengths. _Sources: REF-1_",
                lesson_objective_id=objective_id,
                source_refs=["REF-1"],
            )
        ],
        source_refs=["REF-1"],
    )


# Gates whose slice survives the strip on purpose. The unit id and the carried
# figures are already in the section under repair, and the objective is what the
# section teaches — P1's whole contract is to preserve it.
_UNIT_IDENTITY_GATES = frozenset({"generation_unit", "include_lesson_objectives", None})


def _step_prose_classes() -> tuple[CanaryClass, ...]:
    classes = tuple(canary for canary in CANARY_CLASSES if canary.gate in STEP_PROSE_GATES)
    assert len(classes) == len(STEP_PROSE_GATES) + 1  # both activity classes share a gate
    return classes


def test_canary_tokens_are_mutually_exclusive() -> None:
    """A hit must identify one class: no token may be a substring of another."""
    tokens = [(canary.name, needle) for canary in CANARY_CLASSES for needle in canary.needles]
    for name, needle in tokens:
        for other_name, other in tokens:
            if name == other_name:
                continue
            assert needle not in other, f"{needle!r} ({name}) hides inside {other!r} ({other_name})"


def test_every_context_policy_field_has_a_canary_class() -> None:
    """A new ContextPolicy field is unproven until it is mapped to a plan slice."""
    gates = {canary.gate for canary in CANARY_CLASSES if canary.gate}
    assert gates == set(ContextPolicy.model_fields)


def test_no_canary_class_is_dead() -> None:
    """Each class fires for some real condition, or is pinned as never-carried."""
    for canary in CANARY_CLASSES:
        fires = any(canary.expected(profile) for profile in all_profiles())
        assert fires is (canary.name not in ALWAYS_ABSENT), canary.name


@LEAKAGE
@given(plan=session_plans())
def test_request_carries_exactly_the_slices_the_profile_allows(plan: SessionPlanView) -> None:
    for profile in all_profiles():
        request = build_request(plan, profile)
        probes = {probe: request_probe(request, probe) for probe in ("request", "lesson_context")}
        assert_only_allowed(probes, profile, "request")


@LEAKAGE
@given(plan=session_plans(), profile=condition_profiles())
def test_synthetic_profiles_are_enforced_not_coincidental(
    plan: SessionPlanView, profile: ConditionProfile
) -> None:
    """Flag combinations no registered condition uses must still be obeyed.

    Every registered condition sets ``include_global_lesson_context`` and
    ``include_lesson_objectives`` the same way, so only a profile the registry
    does not contain can show whether the builder reads them.
    """
    request = build_request(plan, profile)
    probes = {probe: request_probe(request, probe) for probe in ("request", "lesson_context")}
    assert_only_allowed(probes, profile, "synthetic request")


@LEAKAGE
@given(plan=session_plans(), profile=condition_profiles())
def test_synthetic_profiles_reach_the_prompt_unchanged(
    plan: SessionPlanView, profile: ConditionProfile
) -> None:
    request = build_request(plan, profile)
    for unit in request.units:
        probes = _prompt_probes(WriteSection, _generate_inputs(request, unit))
        assert_only_allowed(probes, profile, "synthetic prompt", rendered=True)


@pytest.mark.parametrize(
    "profile", EDGE_PROFILES, ids=[profile.description for profile in EDGE_PROFILES]
)
def test_edge_profiles_are_enforced(profile: ConditionProfile) -> None:
    """The flag boundaries a random draw reaches only by luck, pinned deterministically."""
    plan = example_plan()
    request = build_request(plan, profile)
    probes = {probe: request_probe(request, probe) for probe in ("request", "lesson_context")}
    assert_only_allowed(probes, profile, "edge request")
    for unit in request.units:
        assert_only_allowed(
            _prompt_probes(WriteSection, _generate_inputs(request, unit)),
            profile,
            "edge prompt",
            rendered=True,
        )


@LEAKAGE
@given(plan=session_plans(), synthetic=condition_profiles())
def test_evidence_never_exceeds_the_declared_cap(
    plan: SessionPlanView, synthetic: ConditionProfile
) -> None:
    """A condition sees only the evidence its retrieval policy allows.

    Scoped retrieval hands a step its OWN note as a single item, so the cap
    governs the plan-reference fallback rather than the note. A condition that
    provides no evidence must carry none, and no figures either.
    """
    for profile in (*all_profiles(), *EDGE_PROFILES, synthetic):
        request = build_request(plan, profile)
        declared = profile.retrieval.max_evidence_items_per_unit
        # A step unit is handed its own note as one item whatever the cap says;
        # an objective unit falls back to the plan references, which the cap
        # governs literally — zero means zero. Collapsing the two lets a
        # zero-cap condition receive an item with nothing noticing.
        per_step = profile.context.generation_unit == "lesson_step"
        cap = max(declared, 1) if per_step else declared
        for unit in request.units:
            carried = len(unit.source_evidence)
            if not profile.retrieval.provides_evidence:
                assert carried == 0 and unit.source_figures == []
                continue
            assert carried <= cap, f"{profile.condition_code.value}: {carried} items over {cap}"


@PROMPTS
@given(plan=session_plans())
def test_generate_prompt_carries_exactly_the_slices_the_profile_allows(
    plan: SessionPlanView,
) -> None:
    """The C0-C3 prompt the model actually receives, built from a real plan."""
    for profile in h1_profiles():
        request = build_request(plan, profile)
        for unit in request.units:
            probes = _prompt_probes(WriteSection, _generate_inputs(request, unit))
            assert_only_allowed(probes, profile, "generate prompt", rendered=True)


@PROMPTS
@given(plan=session_plans())
def test_repair_prompt_carries_exactly_the_slices_the_profile_allows(
    plan: SessionPlanView,
) -> None:
    """C3's retry path renders a second prompt; it obeys the same profile."""
    retrying = tuple(profile for profile in h1_profiles() if profile.validation.retry_on_failure)
    assert retrying, "no H1 condition repairs — this test would be vacuous"
    for profile in retrying:
        request = build_request(plan, profile)
        for unit in request.units:
            probes = _prompt_probes(
                RepairSection,
                {
                    **_generate_inputs(request, unit),
                    "failed_section": _neutral_section(unit.lesson_objective_id),
                    "validation_issues": ["source_refs_valid: unknown source ref REF-9"],
                },
            )
            assert_only_allowed(probes, profile, "repair prompt", rendered=True)


@PROMPTS
@given(plan=session_plans())
def test_p1_personalise_prompt_carries_no_lesson_plan_step_prose(plan: SessionPlanView) -> None:
    """H2 adapts the approved base pack; the plan's steps never re-enter that path."""
    request = build_request(plan, P1_PROFILE)
    for unit in request.units:
        base_section = _neutral_section(unit.lesson_objective_id)
        probes = _prompt_probes(
            SectionPersonalisation,
            {
                "personalisation_policy": request.policy,
                "lesson_context": request.lesson_context,
                "base_section": base_section,
                "learner_state": ObjectiveLearnerState(
                    lesson_objective_id=unit.lesson_objective_id, mastery_band="remediate"
                ),
                "session_signals": request.session_signals,
                "source_evidence": unit.source_evidence,
            },
        )
        for canary in _step_prose_classes():
            assert not canary.found_in(probes["request"]), (
                f"personalise prompt leaked the {canary.name!r} plan slice"
            )


@PROMPTS
@given(plan=session_plans())
def test_p1_repair_unit_and_prompt_drop_every_step_prose_slice(plan: SessionPlanView) -> None:
    request = build_request(plan, P1_PROFILE)
    for unit in request.units:
        base_section = _neutral_section(unit.lesson_objective_id)
        stripped = unit_for_personalisation_repair(unit, base_section)
        probes = _prompt_probes(
            RepairSection,
            {
                "policy": request.policy,
                "lesson_context": request.lesson_context,
                "unit_context": stripped,
                "source_evidence": stripped.source_evidence,
                "failed_section": base_section,
                "validation_issues": ["no_invented_source_claims: remove the claim"],
            },
        )
        # The slices the H2 unit actually arrives with. Filtering on the profile
        # and skipping the rest emptied this loop entirely: every step-prose class
        # is withheld from P1, so the test asserted nothing and a deleted strip
        # went unnoticed. Assert on what the unit carries, and fail if that is
        # nothing rather than passing vacuously.
        carried = [canary for canary in CANARY_CLASSES if canary.found_in(unit.model_dump_json())]
        plan_slices = [canary for canary in carried if canary.gate not in _UNIT_IDENTITY_GATES]
        assert plan_slices, "the H2 unit carries no plan slice — the strip proves nothing"
        for canary in plan_slices:
            assert not canary.found_in(stripped.model_dump_json()), (
                f"P1 repair unit kept the {canary.name!r} plan slice"
            )
            assert not canary.found_in(probes["request"]), (
                f"P1 repair prompt leaked the {canary.name!r} plan slice"
            )
        # The unit id and the carried figures survive on purpose: the section
        # under repair already carries both (its id is the unit id and the
        # figures were spliced into its blocks), and dropping the figures here
        # would delete them from the repaired section.
        assert stripped.unit_id == unit.unit_id
        assert stripped.source_figures == unit.source_figures


def test_every_context_flag_no_condition_uses_is_a_stated_choice() -> None:
    """A knob the study never turns on has to say why, or come out.

    ``ContextPolicy`` is the declared description of the ablation, so a field
    sitting at False on every registered condition is either a slice deliberately
    withheld — which belongs on the record — or a leftover that reads as a
    manipulation and is none. ``include_timing`` was the second kind: no profile
    could enable it and nothing could have delivered it if one had.

    Asserted as an exact set. The old form named the single flag it knew about,
    so a second leftover would have passed it in silence. The derived gates are
    excluded because they DO deliver — a Gagne code, a step position — just
    nothing a token can find; ``test_derived_slices_follow_their_gate`` holds those.
    """
    unused = {
        canary.gate
        for canary in CANARY_CLASSES
        if canary.gate
        and not canary.derived
        and not any(canary.expected(p) for p in all_profiles())
    }
    assert unused == set(UNUSED_GATES), (
        f"{sorted(unused ^ set(UNUSED_GATES))} changed. A flag no condition turns on needs a "
        "reason here; a flag nothing can deliver needs deleting."
    )


def test_objectives_without_steps_yield_units_only_where_the_unit_is_the_objective() -> None:
    """The generation unit decides what a step-less plan can produce."""
    plan = SessionPlanView.model_validate(
        {"lesson_plan_objectives": [{"lesson_objective_id": "obj0"}], "steps": []}
    )
    for profile in all_profiles():
        expected = 1 if profile.context.generation_unit == "objective" else 0
        assert len(build_request(plan, profile).units) == expected


@LEAKAGE
@given(plan=session_plans(), synthetic=condition_profiles())
def test_derived_slices_follow_their_gate(
    plan: SessionPlanView, synthetic: ConditionProfile
) -> None:
    """The two slices no canary can see must still obey their flag.

    A Gagne code comes from a closed vocabulary the prompt's schema already
    names, and a step position is an integer — so neither can be found by
    searching the payload for the teacher's words. They are checked on the field
    instead, which is the only way these two gates are enforced at all.
    """
    for profile in (*all_profiles(), *EDGE_PROFILES, synthetic):
        context = profile.context
        per_step = context.generation_unit == "lesson_step"
        for unit in build_request(plan, profile).units:
            assert bool(unit.instructional_events) is (
                per_step and context.include_instructional_events
            ), f"{profile.condition_code.value}: instructional_events ignored its gate"
            assert (unit.current_step is not None) is (
                per_step and context.include_lesson_sequence
            ), f"{profile.condition_code.value}: current_step ignored its gate"


def test_the_fixture_can_actually_produce_instructional_events() -> None:
    """Guards the test above from passing because the coder found nothing.

    The coder reads real teaching prose; canary tokens alone code to nothing, so
    a plan of bare tokens would satisfy the gate test in both directions without
    ever exercising the slice.
    """
    profile = profile_for(Hypothesis.H1, ConditionCode.C1)
    events = [
        event
        for unit in build_request(example_plan(), profile).units
        for event in unit.instructional_events
    ]
    assert events, "the fixture's activities code to no events — the gate test is vacuous"


@LEAKAGE
@given(plan=session_plans(), synthetic=condition_profiles())
def test_a_condition_is_never_told_about_a_field_it_was_denied(
    plan: SessionPlanView, synthetic: ConditionProfile
) -> None:
    """Withholding a slice must not announce that the slice exists.

    Serialising the whole model put ``"entry_behaviour": []`` in front of C0 —
    the control arm reading that the field exists and was left empty for it,
    which is the withholding itself made visible. An empty value is therefore a
    leak of shape even when it carries no content.
    """
    for profile in (*all_profiles(), *EDGE_PROFILES, synthetic):
        request = build_request(plan, profile)
        for unit in request.units:
            rendered = shared_inputs(request=request, unit=unit)
            for name in ("lesson_context", "unit_context"):
                empty = [
                    key for key, value in rendered[name].items() if value in ([], {}, "", None)
                ]
                assert not empty, (
                    f"{profile.condition_code.value}: {name} names {empty} with nothing in "
                    "them — the condition is being told which fields it was denied"
                )
            assert all(
                value not in ([], {}, "", None)
                for item in rendered["source_evidence"]
                for value in item.values()
            )
