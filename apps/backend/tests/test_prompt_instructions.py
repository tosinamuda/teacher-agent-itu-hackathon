"""The rules that must reach the model, asserted on the rendered prompt.

A signature docstring is prompt text, so deleting a sentence from one changes
what every run is told and nothing else moves — no schema shifts, no type
breaks, no test fails unless a test reads the prompt. The rules below are the
load-bearing ones: each is either the manipulation itself, a blinding
requirement, or a rule added after a specific failure.

Rendering goes through the same input mappers the generator calls, so this reads
the prompt a run produces rather than one assembled here.
"""

from __future__ import annotations

import dspy
import pytest
from condition_plan_inputs import build_request, example_plan

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
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
    signature_for,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    personalise_inputs,
    repair_inputs,
    shared_inputs,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for

# Each rule, and why removing it would matter. The reason is the point: a rule
# with no consequence does not belong here, and one with a consequence must not
# be deletable in silence.
GENERATION_RULES = (
    (
        "Use ONLY the context given in the inputs",
        "the ablation IS what each condition is given; free recall dissolves it",
    ),
    (
        "ground every claim in it",
        "the C1->C2 manipulation is grounding, not the mere presence of evidence",
    ),
    (
        "never mentions where any of it came from",
        "provenance talk in the prose reaches the rater and names the condition",
    ),
    ("Preserve the given lesson objective", "the objective is the section's scope"),
)

# P1's own rules. The band policy said "easier practice" from the start, but the
# OUTPUT instruction named only blocks — so the model adapted the prose and
# handed the base's questions back word for word, on two independent live draws.
PERSONALISE_RULES = (
    (
        "Return the practice too",
        "the band prescribes the practice as much as the prose; blocks-only "
        "personalisation delivers half the manipulation H2 measures",
    ),
    (
        "easier questions than the base",
        "what remediate MEANS for practice; without it the band is prose-only advice",
    ),
    (
        "Return every block of the base section",
        "a personalised section that drops content is not the same section",
    ),
    (
        "never present problems you wrote as coming from the textbook",
        "P1 authors new items, and attributing them invents provenance",
    ),
)

REPAIR_RULES = (
    (
        "SMALLEST edit",
        "a repair that rewrites freely is a regeneration, and C3's contrast is the repair",
    ),
    (
        "must not appear in the repaired section",
        "a repair that leaves the quoted phrase has not repaired anything",
    ),
    (
        "Never add new claims about where content came from",
        "repair is where invented provenance was observed entering",
    ),
    ("Keep the same lesson objective", "a repair may not change what the section teaches"),
)


def _prose(messages: list[dict]) -> str:
    """The rendered prompt, whitespace-normalised — docstrings wrap across lines."""
    return " ".join("\n".join(str(message["content"]) for message in messages).split())


def _generate_prompt(code: ConditionCode) -> str:
    request = build_request(example_plan(), profile_for(Hypothesis.H1, code))
    return _prose(
        dspy.ChatAdapter().format(
            WriteSection,
            demos=[],
            inputs=shared_inputs(request=request, unit=request.units[0]),
        )
    )


def _personalise_prompt() -> str:
    request = build_request(example_plan(), profile_for(Hypothesis.H2, ConditionCode.P1))
    unit = request.units[0]
    base = ReviewPackSection(
        section_id=unit.unit_id,
        title="t",
        lesson_objective_id=unit.lesson_objective_id,
        blocks=[],
    )
    return _prose(
        dspy.ChatAdapter().format(
            SectionPersonalisation,
            demos=[],
            inputs=personalise_inputs(
                request=request,
                unit=unit,
                base_section=base,
                learner_state=ObjectiveLearnerState(
                    lesson_objective_id=unit.lesson_objective_id, mastery_band="remediate"
                ),
            ),
        )
    )


def _repair_prompt() -> str:
    request = build_request(example_plan(), profile_for(Hypothesis.H1, ConditionCode.C3))
    unit = request.units[0]
    failed = ReviewPackSection(
        section_id=unit.unit_id, title="t", lesson_objective_id=unit.lesson_objective_id, blocks=[]
    )
    return _prose(
        dspy.ChatAdapter().format(
            RepairSection,
            demos=[],
            inputs=repair_inputs(
                request=request, unit=unit, failed_section=failed, issues=["scope_compliance: x"]
            ),
        )
    )


@pytest.mark.parametrize(("rule", "why"), GENERATION_RULES, ids=lambda value: value[:28])
@pytest.mark.parametrize("code", [ConditionCode.C0, ConditionCode.C1, ConditionCode.C3])
def test_the_generation_rules_reach_every_condition(
    code: ConditionCode, rule: str, why: str
) -> None:
    """Every arm is told the same rules — a rule that varies IS a manipulation."""
    assert rule in _generate_prompt(code), f"{code.value} was not told {rule!r}: {why}"


@pytest.mark.parametrize(("rule", "why"), PERSONALISE_RULES, ids=lambda value: value[:28])
def test_the_personalise_rules_reach_the_model(rule: str, why: str) -> None:
    assert rule in _personalise_prompt(), f"the personalise prompt omits {rule!r}: {why}"


@pytest.mark.parametrize(("rule", "why"), REPAIR_RULES, ids=lambda value: value[:28])
def test_the_repair_rules_reach_the_model(rule: str, why: str) -> None:
    assert rule in _repair_prompt(), f"the repair prompt omits {rule!r}: {why}"


#: The lesson-plan fields a codebook can describe, and the context flag that
#: delivers each. A new field fails the tests below until it is mapped here.
FIELD_FLAGS = {
    "entry_behaviour": "include_entry_behaviour",
    "current_step": "include_lesson_sequence",
    "instructional_materials": "include_materials",
    "student_tasks": "include_student_tasks",
    "assessment_points": "include_assessment_points",
    "step_title": "include_step_title",
    "step_content": "include_step_content",
    "activities": "include_teacher_student_activities",
}
FIELD_NAMES = tuple(FIELD_FLAGS)


#: The codebook begins where the instructions first mention the plan at all —
#: the sentence introducing the fields, not the heading below it. Slicing at the
#: heading leaves that sentence counted as task text, which only one condition
#: carries.
CODEBOOK_MARKER = "lesson_context and unit_context may carry"


def _codebook(signature: object) -> str:
    rendered = " ".join(str(signature.instructions).split())  # type: ignore[attr-defined]
    index = rendered.find(CODEBOOK_MARKER)
    return rendered[index:] if index >= 0 else ""


def _entries(codebook: str) -> dict[str, str]:
    """Each field's definition, keyed by field name, in the order they appear."""
    positions = sorted(
        (codebook.index(name), name) for name in FIELD_NAMES if name + " " in codebook
    )
    found: dict[str, str] = {}
    for index, (start, name) in enumerate(positions):
        stop = positions[index + 1][0] if index + 1 < len(positions) else len(codebook)
        found[name] = codebook[start + len(name) : stop].strip()
    return found


def test_a_field_means_the_same_wherever_it_is_described() -> None:
    """A field's DEFINITION may not vary by condition.

    The codebook is rendered per condition now, so the conditions no longer carry
    identical text — a control is not briefed on a plan it will not receive. What
    must not drift is what a field MEANS: two arms reading the same field under
    different definitions would look like a treatment effect.
    """
    seen: dict[str, set[str]] = {}
    for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        book = _codebook(signature_for(profile_for(Hypothesis.H1, code)))
        for name, text in _entries(book).items():
            seen.setdefault(name, set()).add(text)
    drifted = sorted(name for name, texts in seen.items() if len(texts) > 1)
    assert not drifted, f"defined differently by different conditions: {drifted}"


def test_a_condition_is_told_only_about_the_fields_it_carries() -> None:
    """No condition is briefed on an input it cannot receive, or given one unexplained.

    C0 receives no lesson plan and was told what every one of its fields means —
    a control describing the treatment's inputs. It also meant that editing the
    codebook moved the baseline's prompt, so the baseline was not stable.
    """
    for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        profile = profile_for(Hypothesis.H1, code)
        described = set(_entries(_codebook(signature_for(profile))))
        carried = {name for name, flag in FIELD_FLAGS.items() if getattr(profile.context, flag)}
        assert not described - carried, (
            f"{code.value} is told about {sorted(described - carried)}, which it never receives"
        )
        assert not carried - described, (
            f"{code.value} carries {sorted(carried - described)} with nothing saying what they are"
        )


def test_c0_carries_no_lesson_plan_codebook() -> None:
    assert _codebook(signature_for(profile_for(Hypothesis.H1, ConditionCode.C0))) == ""


def test_the_two_h1a_arms_are_asked_the_same_task() -> None:
    """C0 and C1 differ in what they are GIVEN, never in the task they are set.

    Compared on the task text — the instructions with each condition's field
    codebook removed. The codebooks differ by design; the job does not.
    """

    def task(code: ConditionCode) -> str:
        signature = signature_for(profile_for(Hypothesis.H1, code))
        rendered = " ".join(str(signature.instructions).split())
        book = _codebook(signature)
        return (rendered[: rendered.index(book)] if book else rendered).strip()

    assert task(ConditionCode.C0) == task(ConditionCode.C1)
