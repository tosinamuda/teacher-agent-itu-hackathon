"""The study-pack prompts must carry no internal study vocabulary.

Every dspy.Signature docstring, every InputField/OutputField desc, and every
serialized input VALUE is prompt text. Condition/hypothesis labels (C0-C4,
H1/H2, P0/P1), version tags, and date stamps mean nothing to the model — they
must stay on profiles, condition-run rows, and code comments. This renders the
REAL ChatAdapter prompt (the only proof of what the model sees — pydantic
schemas are not) and asserts the jargon is absent.
"""

from __future__ import annotations

import dspy
import pytest

from app.domains.artefacts.types.post_class_review_pack.application.learner_state_input import (
    to_session_signals,
    to_spec_objective_state,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.policy import (
    build_generation_policy,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    LessonContextForGeneration,
    PersonalisedReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.personalise_section import (  # noqa: E501
    SectionPersonalisation,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    personalise_inputs,
    shared_inputs,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.learner_state.domain.models import (
    AnswerEvidence,
    LearnerState,
    ObjectiveLearnerState,
    SessionSurvey,
)
from app.shared.experiment_enums import Hypothesis

FORBIDDEN = (
    '"C0"',
    '"C1"',
    '"C2"',
    '"C3"',
    '"C4"',
    '"H1"',
    '"H2"',
    '"P0"',
    '"P1"',
    "Empty for C0",
    "experimental condition",
    "condition_code",
    "hypothesis",
    "eval-plan",
    "prompt-evidence",
    "v2",
    # Constant per LM call (every personalise call would say "objective_indexed",
    # every generate call "none") — internal vocabulary with no effect on output.
    "personalisation_mode",
    "objective_indexed",
    "reuse_base",
    # Vague key: "status" of what? The band travels as mastery_band.
    '"status"',
    # Bare-number survey keys: three differently-scaled "_score"s with opposite
    # polarities invite cross-scale misreading — values render as anchor
    # phrases instead ("a little sure (2/5)").
    '"mastery_score"',
    '"confidence_score"',
    '"difficulty_score"',
    '"interest_score"',
    # Vague output field name — outputs are named for what they are
    # (section / repaired_section / personalised_section).
    "[[ ## output ## ]]",
)


def _unit() -> SectionGenerationUnit:
    return SectionGenerationUnit(
        unit_id="objective:lop01",
        lesson_objective_id="lop01",
        objective_text="Find the LCM of whole numbers",
    )


def _request(
    condition: ConditionCode, hypothesis: Hypothesis = Hypothesis.H1
) -> BaseReviewPackRequest | PersonalisedReviewPackRequest:
    """A request built by the REAL builder, so the policy prose is the shipped one.

    Hand-building the inputs is how a prompt check reads a prompt no run
    produces — this file did exactly that, passing the raw unit where the
    generator passes ``prompt_unit`` and its own dict where the mappers belong.
    """
    profile = profile_for(hypothesis, condition)
    request_type = (
        BaseReviewPackRequest if hypothesis == Hypothesis.H1 else PersonalisedReviewPackRequest
    )
    return request_type(
        artefact_spec=revision_pack_spec("JSS1"),
        generation_policy=profile.generation_policy(),
        policy=build_generation_policy(profile),
        lesson_context=_lesson_context(),
        units=[_unit()],
        **(
            {"base_pack_id": "PACK-1", "focal_learner_id": "LEARNER-1"}
            if hypothesis == Hypothesis.H2
            else {}
        ),
    )


def _lesson_context() -> LessonContextForGeneration:
    return LessonContextForGeneration(
        subject="Mathematics",
        grade_level="JSS1",
        topic="LCM of whole numbers",
        lesson_objectives=["Find the LCM of whole numbers"],
    )


def _base_section() -> ReviewPackSection:
    return ReviewPackSection(
        section_id="objective:lop01",
        title="Find the LCM",
        lesson_objective_id="lop01",
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="List the multiples of each number.",
                lesson_objective_id="lop01",
            )
        ],
    )


def _render(signature: type[dspy.Signature], inputs: dict) -> str:
    messages = dspy.ChatAdapter().format(signature, demos=[], inputs=inputs)
    return "\n".join(str(message["content"]) for message in messages)


def _assert_clean(prompt: str) -> None:
    hits = [needle for needle in FORBIDDEN if needle in prompt]
    assert not hits, f"internal vocabulary leaked into the prompt: {hits}"


@pytest.mark.parametrize("condition", [ConditionCode.C0, ConditionCode.C2])
def test_generate_prompt_is_jargon_free(condition: ConditionCode) -> None:
    prompt = _render(
        WriteSection,
        shared_inputs(request=_request(condition), unit=_unit()),
    )
    _assert_clean(prompt)


def test_personalise_prompt_is_jargon_free_and_carries_evidence() -> None:
    # Go through the REAL mapper, so the assertions cover the rendering the
    # production paths produce — not a hand-built lookalike.
    domain_state = ObjectiveLearnerState(
        lesson_objective_id="lop01",
        band="remediate",
        mastery_score=0.0,
        questions_correct=0,
        questions_total=2,
        confidence_score=2,
        difficulty_score=5,
        misconception_code="missing_factor_of_two",
        evidence=[
            AnswerEvidence(
                stem="Which is a common multiple of 2 and 3?",
                options={"B": "9", "C": "6"},
                correct_option="C",
                chosen_option="B",
                misconception_code="missing_factor_of_two",
            )
        ],
    )
    learner = LearnerState(student_id="s1", session_survey=SessionSurvey(interest=4, affect=2))
    request = _request(ConditionCode.P1, hypothesis=Hypothesis.H2).model_copy(
        update={"session_signals": to_session_signals(learner)}
    )
    prompt = _render(
        SectionPersonalisation,
        personalise_inputs(
            request=request,
            unit=_unit(),
            base_section=_base_section(),
            learner_state=to_spec_objective_state(domain_state),
        ),
    )
    _assert_clean(prompt)
    # Docstring prose wraps across lines, so prose phrases assert against a
    # whitespace-normalised view; exact JSON keys/values assert against the raw.
    prose = " ".join(prompt.split())
    # The evidence-rich inputs and the behaviour rules must actually be there.
    assert "Which is a common multiple of 2 and 3?" in prompt
    assert '"student_choice": "B"' in prompt
    assert "a common slip" in prose
    assert "never claim" in prose.lower()
    # Semantics must travel via channels that render — pydantic Field
    # descriptions on INPUT models provably do not. Band policy lives in the
    # signature docstring; survey values are self-describing anchor phrases.
    assert '"mastery_band": "remediate"' in prompt
    assert "step-by-step" in prose  # band policy: what "remediate" prescribes
    assert "stretch practice" in prose  # band policy: what "extend" prescribes
    assert "coarse evidence" in prose  # small-denominator caveat
    assert '"mastery": "0 of 2 diagnostic questions correct"' in prompt
    assert '"confidence": "a little sure (2/5)"' in prompt
    assert '"perceived_difficulty": "very difficult (5/5)"' in prompt
    assert '"interest": "interested (4/5)"' in prompt
    assert '"end_of_lesson_feeling": "confused (2/5)"' in prompt
    # Self-describing field names + the problem-provenance rule.
    assert "personalised_section" in prompt
    assert "never present problems you wrote" in prose
