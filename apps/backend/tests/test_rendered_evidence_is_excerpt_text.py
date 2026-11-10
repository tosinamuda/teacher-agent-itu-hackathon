"""The grounded conditions must be taught from content, not from the name of content.

Packs built before 2026-06-11 were grounded in citation labels: the model was handed a
source's name and told to teach only from it. The request object looked right the whole
time, because a label and an excerpt are both a populated string in the same field. This
reads the rendered message instead, through the same `prepared_call` path the snapshots
render, so the two cannot disagree about what was sent.

Refusal to render a grounded contract with no evidence at all is covered by
`test_condition_wire_leakage.py::test_a_grounded_level_refuses_to_render_without_the_evidence_it_teaches_from`,
which also asserts nothing reached the wire. Asserted here only as a boundary of this rule:
empty evidence is a loud failure, not a leak this check has to catch.
"""

from __future__ import annotations

import asyncio

import pytest
from recording_lm import RecordingLM

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from scripts.prompt_snapshots import fixture
from scripts.prompt_snapshots.arms import base_arm, every_arm, personalisation_arm
from scripts.prompt_snapshots.evidence import (
    EVIDENCE_FIELDS,
    label_leaks,
    rendered_evidence,
)

CITATIONS = fixture.SESSION_PLAN.references
GROUNDED = (ConditionCode.C2, ConditionCode.C3)


def _leaks(arm) -> list[str]:
    return label_leaks(rendered_evidence(arm.call), citations=CITATIONS)


@pytest.mark.parametrize("condition", GROUNDED)
def test_a_grounded_condition_is_taught_from_excerpt_text(condition: ConditionCode) -> None:
    arm = base_arm(condition)
    items = rendered_evidence(arm.call)

    assert items, f"{condition.value} is a grounded condition and sent no evidence"
    assert _leaks(arm) == []


def test_every_arm_that_sends_evidence_sends_content_not_labels() -> None:
    """Including P1, which is grounded through the same projection."""
    offenders = {
        arm.condition.value: leaks
        for arm in every_arm()
        if arm.call is not None and (leaks := _leaks(arm))
    }
    assert offenders == {}


def test_the_check_reads_the_rendered_message_not_the_request() -> None:
    """A label leak is invisible in the request: both readings are a populated string."""
    arm = base_arm(ConditionCode.C2)
    note = fixture.SESSION_PLAN.steps[0].note

    assert note is not None
    assert any(item["excerpt"].strip() == note.strip() for item in rendered_evidence(arm.call))


def test_p1_is_taught_from_excerpt_text_too() -> None:
    arm = personalisation_arm(ConditionCode.P1)

    assert arm.call is not None
    assert _leaks(arm) == []


def test_an_unresolved_citation_reaching_the_prompt_is_caught() -> None:
    """The guard must bite, or it only asserts that today happens to be fine.

    `LessonSources.unresolved` sets a source's content to its own citation, and a step with
    nothing of its own falls back to those plan-level sources. That is the 2026-06-11 leak
    exactly, and it renders as a populated `excerpt` carrying a book title.

    Both the note and the blocks have to go: step evidence reads the note first, then the
    text of the step's blocks, and only an empty step reaches the plan sources.
    """
    plan = fixture.SESSION_PLAN.model_copy(
        update={
            "steps": [
                step.model_copy(update={"note": None, "blocks": []})
                for step in fixture.SESSION_PLAN.steps
            ]
        }
    )
    request = BaseReviewPackRequestBuilder().build(
        session_plan=plan,
        policy=profile_for(Hypothesis.H1, ConditionCode.C2).generation_policy(),
        sources=fixture.LESSON_SOURCES,
    )
    call = GenerateSection(lm=RecordingLM([])).prepared_call(request=request, unit=request.units[0])

    leaks = label_leaks(rendered_evidence(call), citations=CITATIONS)

    assert leaks, "a citation label reached the prompt as evidence and the guard missed it"
    assert "not an excerpt of it" in leaks[0]


def test_the_evidence_fields_are_the_ones_the_contracts_declare() -> None:
    """A new evidence field must be added here, or it goes unchecked."""
    declared = {
        name
        for arm in every_arm()
        if arm.call is not None
        for name in arm.call.contract.input_fields
        if "evidence" in name or "content" in name
    }
    assert declared <= set(EVIDENCE_FIELDS)


def test_empty_evidence_is_a_loud_failure_not_a_silent_label() -> None:
    """The boundary of this rule: nothing to teach from must raise, never render."""
    request = BaseReviewPackRequestBuilder().build(
        session_plan=fixture.SESSION_PLAN,
        policy=profile_for(Hypothesis.H1, ConditionCode.C2).generation_policy(),
        sources=fixture.LESSON_SOURCES,
    )
    stripped = request.model_copy(
        update={
            "units": [unit.model_copy(update={"source_evidence": []}) for unit in request.units]
        }
    )
    generator = GenerateSection(lm=RecordingLM([]), contract_mode="leveled")

    with pytest.raises(ValueError, match="teaches only from lesson_content"):
        asyncio.run(generator.generate_section(request=stripped, unit=stripped.units[0]))
