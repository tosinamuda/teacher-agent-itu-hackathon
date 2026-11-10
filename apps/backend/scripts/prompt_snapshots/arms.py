"""One prepared model call per condition arm, built from the fixed lesson.

The call is built by the generator itself rather than reassembled here, so a snapshot
always describes a call the generator would actually make. These render
``GenerateSection``'s shared contract, which pins what each condition's request carries.
The prompt production serves comes from ``ComposeSection`` and is pinned by ``served.py``.

P0 appears with no call. Its policy reuses the approved base sections unchanged, so no
prompt exists to snapshot — recorded as a fact rather than an omission.
"""

from __future__ import annotations

from dataclasses import dataclass

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.personalised.builder import (  # noqa: E501
    PersonalisedReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prepared_call import (
    PreparedCall,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from scripts.prompt_snapshots import fixture

BASE_CONDITIONS = (
    ConditionCode.C0,
    ConditionCode.C1,
    ConditionCode.C2,
    ConditionCode.C3,
)


class _UncallableLM(dspy.BaseLM):
    """Stands where a provider would. Rendering must never reach the wire."""

    def __init__(self) -> None:
        super().__init__(model="prompt-snapshot/no-provider")

    def forward(self, *args: object, **kwargs: object) -> object:
        raise AssertionError("rendering a prompt snapshot must not call a model")


@dataclass(frozen=True)
class Arm:
    """One condition's prompt, or the recorded fact that it sends none."""

    condition: ConditionCode
    description: str
    call: PreparedCall | None


def base_arm(condition: ConditionCode) -> Arm:
    """The base-generation call C0-C3 make for the fixture's first unit."""
    profile = profile_for(Hypothesis.H1, condition)
    request = BaseReviewPackRequestBuilder().build(
        session_plan=fixture.SESSION_PLAN,
        policy=profile.generation_policy(),
        sources=fixture.LESSON_SOURCES,
    )
    generator = GenerateSection(lm=_UncallableLM())
    return Arm(
        condition=condition,
        description=profile.description,
        call=generator.prepared_call(request=request, unit=request.units[0]),
    )


def personalisation_arm(condition: ConditionCode) -> Arm:
    """P1's personalisation call, or P0's absence of one."""
    profile = profile_for(Hypothesis.H2, condition)
    policy = profile.generation_policy()
    if not policy.personalisation.adapts_to_learner_state:
        return Arm(condition=condition, description=profile.description, call=None)

    request = PersonalisedReviewPackRequestBuilder().build(
        session_plan=fixture.SESSION_PLAN,
        base_pack_id="pack-base-1",
        focal_learner_id="learner-1",
        learner_states={fixture.FIRST_OBJECTIVE_ID: fixture.LEARNER_STATE},
        policy=policy,
        session_signals=fixture.SESSION_SIGNALS,
        sources=fixture.LESSON_SOURCES,
    )
    personaliser = PersonaliseSection(lm=_UncallableLM())
    return Arm(
        condition=condition,
        description=profile.description,
        call=personaliser.prepared_call(
            request=request,
            unit=request.units[0],
            base_section=fixture.BASE_SECTION,
            learner_state=fixture.LEARNER_STATE,
        ),
    )


def every_arm() -> list[Arm]:
    """Every arm this snapshot covers, in the order the study names them."""
    return [base_arm(condition) for condition in BASE_CONDITIONS] + [
        personalisation_arm(ConditionCode.P0),
        personalisation_arm(ConditionCode.P1),
    ]
