"""Per-level signatures: fields accumulate, absence is real, and the TASK never varies.

Two things pinned here. At a level with no evidence, the evidence field is ABSENT from
the rendered prompt — no roster line, no empty value — versus the shared signature where
it rides along empty everywhere. And C0 and C1 receive an identical instruction, so the
contrast between them is the lesson-plan data and nothing else.
"""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteGroundedSection,
    WriteObjectiveSection,
    signature_for,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for


def test_levels_map_by_what_the_profile_provides() -> None:
    """The level follows the evidence policy; the codebook follows the context.

    Compared by input fields rather than identity: a signature is built per
    condition now, because a condition is told about its own fields and no others.
    """
    for code in (ConditionCode.C0, ConditionCode.C1):
        built = signature_for(profile_for(Hypothesis.H1, code))
        assert set(built.input_fields) == set(WriteObjectiveSection.input_fields)
    for code in (ConditionCode.C2, ConditionCode.C3):
        built = signature_for(profile_for(Hypothesis.H1, code))
        assert set(built.input_fields) == set(WriteGroundedSection.input_fields)


def test_c0_and_c1_are_told_exactly_the_same_thing() -> None:
    """H1a is C1 vs C0, so anything said to one and not the other is the confound.

    They ran different signatures until 2026-08-09: C1's said "teaching this step of the
    lesson … teach this part and leave the rest to its own section", a narrowing
    instruction the baseline never saw. Their units are 1:1 regardless — the validator
    requires exactly one core step per objective — so the split bought nothing and cost
    construct isolation.
    """
    c0 = signature_for(profile_for(Hypothesis.H1, ConditionCode.C0))
    c1 = signature_for(profile_for(Hypothesis.H1, ConditionCode.C1))
    # The TASK, not the whole instructions: C1's codebook describes the fields C1
    # receives, and C0 has none to describe. C0 was previously told what a lesson
    # plan's fields mean and then given none of them.
    marker = "lesson_context and unit_context may carry"
    task = lambda s: str(s.instructions).split(marker)[0].strip()  # noqa: E731
    assert task(c0) == task(c1)
    assert set(c0.input_fields) == set(c1.input_fields)
    assert marker not in str(c0.instructions)


def test_the_instructional_events_codebook_reaches_every_level_that_carries_them() -> None:
    """The legend goes to every condition that receives the events, and no other.

    A legend given to one condition and withheld from another that has the same
    field would itself be a treatment. A legend given to a condition without the
    field describes an input it cannot receive.
    """
    for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        profile = profile_for(Hypothesis.H1, code)
        instructions = str(signature_for(profile).instructions)
        carries = profile.context.include_instructional_events
        assert ("stimulate_recall" in instructions) is carries, code.value
        assert ("provide_learning_guidance" in instructions) is carries, code.value


def test_an_evidence_level_gains_a_field_not_a_different_task() -> None:
    assert "lesson_content" not in WriteObjectiveSection.input_fields
    assert "lesson_content" in WriteGroundedSection.input_fields


def test_absent_field_renders_no_roster_line_and_no_empty_value() -> None:
    inputs = {
        "artefact_spec": revision_pack_spec("JSS1"),
        "lesson_context": LessonContextForGeneration(
            subject="Mathematics", grade_level="JSS1", topic="Addition", lesson_objectives=["add"]
        ),
        "unit_context": {"lesson_objective_id": "lop01", "objective_text": "add"},
    }
    rendered = "\n".join(
        m["content"] for m in dspy.ChatAdapter().format(WriteObjectiveSection, [], inputs)
    )
    assert "lesson_content" not in rendered
    assert "source_evidence" not in rendered
    assert "policy" not in rendered  # the level's docstring IS the condition
    assert WriteObjectiveSection.instructions.splitlines()[0] in rendered


def test_every_lesson_plan_field_has_a_defined_meaning() -> None:
    """Otherwise the study partly measures whether a model can guess our JSON key names.

    ``instructional_events`` had a codebook while five sibling fields were bare keys.
    Each now states its role, identically for every condition — the values differ, the
    legend never does.
    """
    for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        profile = profile_for(Hypothesis.H1, code)
        contract = str(signature_for(profile).instructions)
        for field, flag in (
            ("entry_behaviour", "include_entry_behaviour"),
            ("current_step", "include_lesson_sequence"),
            ("instructional_materials", "include_materials"),
            ("student_tasks", "include_student_tasks"),
            ("assessment_points", "include_assessment_points"),
            ("instructional_events", "include_instructional_events"),
        ):
            # Described exactly when delivered: a bare key is a guess, and a
            # definition for a field that never arrives is a control being told
            # about the treatment.
            assert (field in contract) is getattr(profile.context, flag), (code.value, field)


def test_the_objective_outranks_the_assessment_points() -> None:
    """An evaluation item may not redefine the objective it was written to check.

    `t3-w09` assesses "state three methods of collecting data" against an objective of
    "analyse and interpret statistical data presented in tables". Without a stated
    hierarchy every plan field carried equal authority to redirect the section.
    """
    # Read off C1, which receives the assessment points the hierarchy governs.
    contract = " ".join(
        str(signature_for(profile_for(Hypothesis.H1, ConditionCode.C1)).instructions).split()
    )
    assert "it sets the section's scope" in contract
    assert "it does not narrow or replace what this section teaches" in contract
