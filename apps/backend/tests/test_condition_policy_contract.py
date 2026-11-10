"""What a profile declares must survive into the rules the model is given.

The leakage suites prove the request carries the right lesson-plan slices. This
proves the other half of the manipulation: the instruction text that travels
with them, the derived personalisation properties consumers branch on, and the
immutability of the registry itself. A condition whose payload is right but
whose instruction belongs to a different condition is still a broken condition.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    learner_setting,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.policy import (
    build_generation_policy,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    BASE_REVIEW_PACK_POLICY,
    PERSONALISED_REVIEW_PACK_POLICY,
    as_the_study_ran_it,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import (
    ConditionProfile,
    condition_codes,
    profile_for,
)
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant

# Each instruction sentence, and the profile question that decides whether the
# model is told it. Read off the profile so a registry edit moves the
# expectation with it.
INSTRUCTIONS: tuple[tuple[str, str], ...] = (
    ("Generate the section from the context supplied for this unit.", "always"),
    ("Ground every claim in the provided source evidence", "retrieval"),
    ("Never write a source marker, reference number or citation in the", "source_refs"),
    ("Use only the provided evidence; do not invent sources.", "only_provided"),
    ("Adapt the base section to the learner state", "personalises"),
)

PROFILE_MODELS = ("context", "retrieval", "validation", "teacher_validation", "personalisation")


def _all_profiles() -> list[ConditionProfile]:
    return [
        profile_for(hypothesis, code)
        for hypothesis in (Hypothesis.H1, Hypothesis.H2)
        for code in condition_codes(hypothesis)
    ]


def _expects(profile: ConditionProfile, rule: str) -> bool:
    return {
        "always": True,
        "retrieval": profile.retrieval.enabled,
        "source_refs": profile.retrieval.enabled and profile.retrieval.require_source_refs,
        "only_provided": profile.retrieval.enabled and profile.retrieval.use_only_provided_sources,
        "personalises": profile.personalisation.adapts_to_learner_state,
    }[rule]


def test_the_two_h1a_arms_are_asked_to_write_the_same_thing() -> None:
    """C0 and C1 differ in what they are TOLD about the lesson, never in the task.

    The instruction used to branch on unit kind, which made the primary
    comparison a task difference as well as a context one.
    """
    c0 = build_generation_policy(profile_for(Hypothesis.H1, ConditionCode.C0))
    c1 = build_generation_policy(profile_for(Hypothesis.H1, ConditionCode.C1))
    assert c0.instruction_summary == c1.instruction_summary


@pytest.mark.parametrize("profile", _all_profiles(), ids=lambda p: p.condition_code.value)
def test_instruction_summary_states_exactly_this_condition_rules(
    profile: ConditionProfile,
) -> None:
    """The in-prompt rules must match the payload the same profile produced.

    An inverted branch here hands C0 the lesson-plan instruction and C1-C3 the
    objective-only one while every request assertion still passes — a
    condition inversion that is invisible outside the prompt text.
    """
    summary = build_generation_policy(profile).instruction_summary
    for sentence, rule in INSTRUCTIONS:
        assert (sentence in summary) is _expects(profile, rule), (
            f"{profile.condition_code.value}: {sentence!r} should "
            f"{'be' if _expects(profile, rule) else 'not be'} in {summary!r}"
        )


def test_personalisation_properties_are_not_interchangeable() -> None:
    """P0 reuses the base; P1 adapts it. Consumers branch on these, not the mode."""
    p0 = profile_for(Hypothesis.H2, ConditionCode.P0).personalisation
    p1 = profile_for(Hypothesis.H2, ConditionCode.P1).personalisation
    assert p0.reuses_base_sections is True
    assert p0.adapts_to_learner_state is False
    assert p1.reuses_base_sections is False
    assert p1.adapts_to_learner_state is True


def test_production_policies_match_the_study_treatments_that_were_rated() -> None:
    """The class note as the rated Part 1 run wrote C3 — context variant v7-full, not the
    frozen v3 — and a learner's note as Part 2 wrote P1, apart from the checks added since."""
    rated_c3 = profiles_for_variant("v7-full")[ConditionCode.C3]
    assert rated_c3.generation_policy() == as_the_study_ran_it(BASE_REVIEW_PACK_POLICY)
    assert profile_for(Hypothesis.H2, ConditionCode.P1).generation_policy() == as_the_study_ran_it(
        PERSONALISED_REVIEW_PACK_POLICY
    )


def test_the_class_note_sends_the_teachers_drawings_as_part_1_did() -> None:
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (  # noqa: E501
        build_base_review_pack_generator,
        section_collaborators,
    )

    generator = build_base_review_pack_generator(section_collaborators(object()))  # type: ignore[arg-type]

    assert generator._request_builder._figures == "source"


def test_p1_declares_retry_and_objective_preservation() -> None:
    """P1's two silent guarantees: a failed pack is repaired, the objective is kept."""
    p1 = profile_for(Hypothesis.H2, ConditionCode.P1)
    assert p1.validation.enabled is True
    assert p1.validation.retry_on_failure is True
    assert p1.personalisation.preserve_base_objectives is True
    policy = build_generation_policy(p1)
    assert policy.preserve_lesson_objective is True


@pytest.mark.parametrize("profile", _all_profiles(), ids=lambda p: p.condition_code.value)
@pytest.mark.parametrize("model_name", PROFILE_MODELS)
def test_condition_profiles_cannot_be_mutated_at_runtime(
    profile: ConditionProfile, model_name: str
) -> None:
    """Profiles are module-level singletons shared by every run in the process.

    One in-place write would redefine a condition for every later run in that
    worker, and the persisted ``condition_profile`` would record the change as
    though it had always been so.
    """
    policy = getattr(profile, model_name)
    field = next(iter(type(policy).model_fields))
    with pytest.raises(ValidationError):
        setattr(policy, field, None)


# The grade bands the study runs over, and what each one must name.
JSS_GRADES = ("JSS1", "JSS2", "JSS3")


@pytest.mark.parametrize("grade", JSS_GRADES)
def test_the_learner_setting_names_the_curriculum_not_just_the_grade(grade: str) -> None:
    """ "JSS1" alone tells a reader nothing unless they know the system.

    Neither model did: the critic marked "mathematical set" false because it is
    not the phrase it expects for a geometry set, though it is the standard one
    here and the teacher's own word. The setting exists to say which curriculum
    a section is written for, so a grade with no curriculum behind it is the
    regression.
    """
    setting = learner_setting(
        LessonContextForGeneration(
            subject="Mathematics", grade_level=grade, topic="Angles", lesson_objectives=["o1"]
        )
    )
    assert grade in setting
    assert "Nigerian" in setting and "NERDC" in setting


def test_an_unknown_grade_still_says_what_it_knows() -> None:
    """A grade outside the mapped bands names no curriculum rather than a wrong one."""
    setting = learner_setting(
        LessonContextForGeneration(
            subject="Mathematics", grade_level="SS2", topic="Angles", lesson_objectives=["o1"]
        )
    )
    assert setting == "SS2"


def test_a_missing_grade_is_said_out_loud() -> None:
    """Silence would read as a deliberate choice not to state the setting."""
    setting = learner_setting(
        LessonContextForGeneration(
            subject="Mathematics", grade_level="", topic="Angles", lesson_objectives=["o1"]
        )
    )
    assert setting == ""


def test_a_learner_section_is_held_to_the_explanation_floor_the_study_did_not_apply() -> None:
    assert "explanation_present" in PERSONALISED_REVIEW_PACK_POLICY.validation.checks
    studied = as_the_study_ran_it(PERSONALISED_REVIEW_PACK_POLICY)
    assert "explanation_present" not in studied.validation.checks
