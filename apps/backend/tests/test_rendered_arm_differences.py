"""What separates the arms, stated as a table over the rendered prompts.

A claim about why an arm wins rests on what that arm was shown, so the difference has to be
asserted from the render rather than read off the profile definitions — the profiles say
what a condition MAY carry, and the two have disagreed before.

Under the shared contract production binds, all four H1 arms send the same five signature
fields. So the manipulation is one level down: the keys inside `lesson_context` and
`unit_context`, and whether evidence arrived with anything in it. That is what this table
pins, and equalising two arms by editing a profile fails it.
"""

from __future__ import annotations

import pytest

from scripts.prompt_snapshots.arms import every_arm
from scripts.prompt_snapshots.field_map import EVIDENCE_KEY, receiving_conditions
from scripts.prompt_snapshots.rendered import user_message

ARMS = every_arm()
BY_CODE = {arm.condition.value: arm for arm in ARMS}

ALL_BASE = frozenset({"C0", "C1", "C2", "C3"})
PLAN_ARMS = frozenset({"C1", "C2", "C3"})
GROUNDED = frozenset({"C2", "C3"})

# Read off the renders, then written down. Regenerate the left column with
# `receiving_conditions(every_arm())` when a field is deliberately added or moved.
EXPECTED: dict[str, frozenset[str]] = {
    # Curriculum specification — every H1 arm, and P1 through the same projection.
    "lesson_context.curriculum_scope": ALL_BASE | {"P1"},
    "lesson_context.grade_level": ALL_BASE | {"P1"},
    "lesson_context.lesson_objectives": ALL_BASE | {"P1"},
    "lesson_context.subject": ALL_BASE | {"P1"},
    "lesson_context.subtopic": ALL_BASE | {"P1"},
    "lesson_context.term": ALL_BASE | {"P1"},
    "lesson_context.topic": ALL_BASE | {"P1"},
    "lesson_context.week": ALL_BASE | {"P1"},
    "unit_context.objective_text": ALL_BASE,
    # The lesson plan — this is the C0/C1 manipulation, and all of it.
    "lesson_context.entry_behaviour": PLAN_ARMS | {"P1"},
    "lesson_context.instructional_materials": PLAN_ARMS | {"P1"},
    "unit_context.assessment_points": PLAN_ARMS,
    "unit_context.current_step": PLAN_ARMS,
    "unit_context.instructional_events": PLAN_ARMS,
    "unit_context.student_tasks": PLAN_ARMS,
    # The evidence step — what H1 attributed C3's win to.
    EVIDENCE_KEY: GROUNDED | {"P1"},
    # Learner state — the H2 manipulation, and no H1 arm may see it.
    "learner_state.confidence": frozenset({"P1"}),
    "learner_state.evidence_items": frozenset({"P1"}),
    "learner_state.mastery": frozenset({"P1"}),
    "learner_state.mastery_band": frozenset({"P1"}),
    "learner_state.misconception": frozenset({"P1"}),
    "learner_state.perceived_difficulty": frozenset({"P1"}),
    "session_signals.end_of_lesson_feeling": frozenset({"P1"}),
    "session_signals.interest": frozenset({"P1"}),
}


def test_each_field_reaches_exactly_the_conditions_the_study_declares() -> None:
    assert receiving_conditions(ARMS) == EXPECTED


def test_the_evidence_step_is_one_of_the_pinned_differences() -> None:
    """C3's advantage was attributed to evidence, so evidence must be asserted, not assumed."""
    assert EXPECTED[EVIDENCE_KEY] == GROUNDED | {"P1"}
    assert "C0" not in EXPECTED[EVIDENCE_KEY]
    assert "C1" not in EXPECTED[EVIDENCE_KEY]


def test_no_h1_arm_is_shown_learner_state() -> None:
    """H1 is a base-pack hypothesis; a learner field reaching it would confound both."""
    leaked = {
        key: sorted(who & ALL_BASE)
        for key, who in EXPECTED.items()
        if key.startswith(("learner_state.", "session_signals.")) and who & ALL_BASE
    }
    assert leaked == {}


@pytest.mark.parametrize(
    ("left", "right", "what_separates_them"),
    [
        ("C0", "C1", "the lesson plan"),
        ("C1", "C2", "the evidence step"),
    ],
)
def test_a_profile_change_that_equalised_these_arms_would_fail(
    left: str, right: str, what_separates_them: str
) -> None:
    """The comparison is over the sent bytes, so equalising the values fails too.

    A field map alone would pass if a profile kept a key but emptied it.
    """
    assert user_message(BY_CODE[left].call) != user_message(BY_CODE[right].call), (
        f"{left} and {right} now send the same prompt: "
        f"{what_separates_them} stopped separating them"
    )


def test_c2_and_c3_send_the_same_prompt_and_that_is_not_a_bug() -> None:
    """Recorded so a reader does not go looking for a prompt difference that never existed.

    C3 adds validation and repair AFTER generation. Nothing separating it from C2 is
    anything the model is shown, so an attribution of C3's win to its prompt is unavailable.
    """
    assert user_message(BY_CODE["C2"].call) == user_message(BY_CODE["C3"].call)


def test_p0_is_shown_nothing_because_it_is_sent_nothing() -> None:
    assert BY_CODE["P0"].call is None
