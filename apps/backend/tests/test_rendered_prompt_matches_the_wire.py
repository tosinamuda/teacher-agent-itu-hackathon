"""The snapshots must be the bytes, not a faithful-looking reconstruction of them.

`PreparedCall.messages()` formats with a `ChatAdapter` it builds itself. That is one
`acall` argument list away from the truth, and this codebase has already paid for that gap
once: a jargon check assembled its own inputs, passed for months, and C0 was handed the
fields it is denied the entire time.

So the render is held against the wire. `RecordingLM` replaces the provider, leaving every
line of the generator in the call path, and what it receives must equal what the snapshot
prints. If DSPy ever formats differently from how this package renders — a configured
adapter, demos injected by an optimizer, a kwarg that changes serialisation — these fail
rather than the snapshots quietly describing a call nobody makes.
"""

from __future__ import annotations

import asyncio

import pytest
from recording_lm import RecordingLM, completion

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.personalised.builder import (  # noqa: E501
    PersonalisedReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    DraftBlock,
    DraftPractice,
    DraftSection,
    RevisedSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    ContractMode,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from scripts.prompt_snapshots import fixture


def _draft() -> DraftSection:
    return DraftSection(
        title="Distance round a rectangle",
        instructional_support="Add every side, or double the length plus the breadth.",
        worked_examples=[DraftBlock(block_type="worked_example", text="2 x (8 + 5) = 26 cm")],
        practice=[DraftPractice(prompt="A 7 cm by 4 cm rectangle.", answer="22 cm")],
    )


def _revision() -> RevisedSection:
    return RevisedSection(
        title="Distance round a rectangle",
        blocks=[DraftBlock(block_type="worked_example", text="2 x (8 + 5) = 26 cm")],
        practice=[DraftPractice(prompt="A 7 cm by 4 cm rectangle.", answer="22 cm")],
    )


def _base_request(condition: ConditionCode):
    return BaseReviewPackRequestBuilder().build(
        session_plan=fixture.SESSION_PLAN,
        policy=profile_for(Hypothesis.H1, condition).generation_policy(),
        sources=fixture.LESSON_SOURCES,
    )


def _rendered(call) -> list[str]:
    return [message["content"] for message in call.messages()]


@pytest.mark.parametrize("contract_mode", ["shared", "leveled"])
@pytest.mark.parametrize("condition", [ConditionCode.C1, ConditionCode.C2])
def test_the_base_render_is_what_the_provider_receives(
    condition: ConditionCode, contract_mode: ContractMode
) -> None:
    request = _base_request(condition)
    lm = RecordingLM(completion(section=_draft()))
    generator = GenerateSection(lm=lm, contract_mode=contract_mode)

    rendered = _rendered(generator.prepared_call(request=request, unit=request.units[0]))
    asyncio.run(generator.generate_section(request=request, unit=request.units[0]))

    assert lm.messages_per_call == [rendered]


def test_the_personalisation_render_is_what_the_provider_receives() -> None:
    request = PersonalisedReviewPackRequestBuilder().build(
        session_plan=fixture.SESSION_PLAN,
        base_pack_id="pack-base-1",
        focal_learner_id="learner-1",
        learner_states={fixture.FIRST_OBJECTIVE_ID: fixture.LEARNER_STATE},
        policy=profile_for(Hypothesis.H2, ConditionCode.P1).generation_policy(),
        session_signals=fixture.SESSION_SIGNALS,
        sources=fixture.LESSON_SOURCES,
    )
    lm = RecordingLM(completion(personalised_section=_revision()))
    personaliser = PersonaliseSection(lm=lm)
    arguments = {
        "request": request,
        "unit": request.units[0],
        "base_section": fixture.BASE_SECTION,
        "learner_state": fixture.LEARNER_STATE,
    }

    rendered = _rendered(personaliser.prepared_call(**arguments))
    asyncio.run(personaliser.personalise_section(**arguments))

    assert lm.messages_per_call == [rendered]


def test_preparing_a_call_sends_nothing() -> None:
    """Rendering must stay free: the snapshots regenerate in CI, on every arm."""
    request = _base_request(ConditionCode.C2)
    lm = RecordingLM()

    GenerateSection(lm=lm).prepared_call(request=request, unit=request.units[0]).messages()

    assert lm.sent == []
