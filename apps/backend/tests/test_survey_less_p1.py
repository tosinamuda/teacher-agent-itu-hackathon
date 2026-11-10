"""FD-05: P1 personalisation runs on a survey-less learner state.

The field-deployment flow collects no post-class survey, so the learner state
carries band + misconception but no confidence/perceived-difficulty/session signals.
These pin that the P1 prompt renders cleanly (no error, no dangling instruction) and
that objective_preservation — the survey-independent output check — still works.
"""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    GenerationPolicyContext,
    LessonContextForGeneration,
    ObjectiveLearnerState,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.personalise_section import (  # noqa: E501
    SectionPersonalisation,
)


def _section(objective_id: str) -> ReviewPackSection:
    return ReviewPackSection(
        section_id="sec",
        title="Solving linear equations",
        lesson_objective_id=objective_id,
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="To solve 5x = 20, divide both sides by 5.",
                lesson_objective_id=objective_id,
            )
        ],
    )


def test_p1_prompt_renders_survey_less_state_without_dangling_instructions() -> None:
    # Band + misconception only; no survey signals.
    learner_state = ObjectiveLearnerState(
        lesson_objective_id="lop01",
        mastery_band="remediate",
        mastery="0 of 2 diagnostic questions correct",
        confidence=None,
        perceived_difficulty=None,
        misconception="divides_instead_of_multiplies",
        evidence_items=[],
    )
    inputs = {
        "personalisation_policy": GenerationPolicyContext(
            require_source_refs=False,
            use_only_provided_sources=False,
            preserve_lesson_objective=True,
            instruction_summary="Adapt depth to the mastery band.",
        ),
        "lesson_context": LessonContextForGeneration(
            subject="Mathematics",
            grade_level="JSS1",
            topic="Equations",
            lesson_objectives=["Solve one-step linear equations"],
        ),
        "base_section": _section("lop01"),
        "learner_state": learner_state,
        "session_signals": None,
        "source_evidence": [],
    }

    messages = dspy.ChatAdapter().format(SectionPersonalisation, demos=[], inputs=inputs)
    user = "\n\n".join(message["content"] for message in messages if message["role"] == "user")

    # Band + misconception reach the model; the absent survey answers render as
    # explicit nulls, never as a half-written "Confidence: " instruction.
    assert "remediate" in user
    assert "divides_instead_of_multiplies" in user
    assert '"confidence": null' in user
    assert '"perceived_difficulty": null' in user


def test_objective_preservation_passes_independent_of_survey() -> None:
    validator = ReviewPackStructuralValidator()
    # Same objective in base + candidate → preserved (survey never enters this check).
    preserved = validator._objective_preservation([_section("lop01")], [_section("lop01")])  # noqa: SLF001
    assert preserved.passed
    # Dropping the objective is the only way this check fails.
    dropped = validator._objective_preservation([], [_section("lop01")])  # noqa: SLF001
    assert not dropped.passed
