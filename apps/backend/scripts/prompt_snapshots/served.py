"""The first message list production's section composer sends, for each base condition.

``arms.py`` renders ``GenerateSection``'s shared contract. Production writes a section
through ``ComposeSection`` over ``dspy.ReActV2`` instead, whose first turn wraps the
leveled contract in the agent loop's own fields and lists the composition tools. Only a
render of that turn shows what a C0-C3 section call actually puts in front of the model.

The composer is built by ``section_collaborators`` — the factory production uses — over a
model that records the first request it receives and refuses it. Nothing is reassembled
here, so the snapshot cannot describe a call production would not make.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import dspy

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (  # noqa: E501
    ComposeSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    section_collaborators,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from scripts.prompt_snapshots import fixture
from scripts.prompt_snapshots.arms import BASE_CONDITIONS


class _RefusedError(Exception):
    """Raised in place of a provider response, once the request is recorded."""


class _RecordingLM(dspy.BaseLM):
    """Keeps the first request it is sent and answers none of them."""

    def __init__(self) -> None:
        super().__init__(model="prompt-snapshot/recorder", cache=False)
        self.first: list[dict[str, str]] | None = None
        self.options: dict[str, object] = {}

    def forward(self, prompt=None, messages=None, **kwargs):  # type: ignore[no-untyped-def]
        if self.first is None:
            self.first = messages
            self.options = kwargs
        raise _RefusedError

    async def aforward(self, prompt=None, messages=None, **kwargs):  # type: ignore[no-untyped-def]
        return self.forward(prompt=prompt, messages=messages, **kwargs)


@dataclass(frozen=True)
class ServedArm:
    """One condition's first composition turn, as production sends it."""

    condition: ConditionCode
    description: str
    contract: str
    messages: list[dict[str, str]]
    options: dict[str, object]


def _was_refused(error: BaseException | None) -> bool:
    while error is not None:
        if isinstance(error, _RefusedError):
            return True
        error = error.__cause__ or error.__context__
    return False


def served_arm(
    condition: ConditionCode,
    specification: ContentSpecification | None = None,
    pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
) -> ServedArm:
    """Record the first request production's composer makes for the fixture's first unit.

    ``specification`` is a stored revision; without one the seed revision is used.
    """
    profile = profile_for(Hypothesis.H1, condition)
    request = BaseReviewPackRequestBuilder().build(
        session_plan=fixture.SESSION_PLAN,
        policy=profile.generation_policy(),
        sources=fixture.LESSON_SOURCES,
        specification=specification,
    )
    lm = _RecordingLM()
    composer = section_collaborators(lm, pipeline).generator
    assert isinstance(composer, ComposeSection), "production no longer composes sections"
    try:
        asyncio.run(composer.generate_section(request=request, unit=request.units[0]))
    except Exception as error:  # noqa: BLE001 - only the recorder's own refusal is expected
        if not _was_refused(error):
            raise
    if lm.first is None:
        raise AssertionError(f"{condition.value}: the composer finished without calling the model")
    return ServedArm(
        condition=condition,
        description=profile.description,
        contract=composer.contract(request).__name__,
        messages=lm.first,
        options=lm.options,
    )


def every_served_arm() -> list[ServedArm]:
    """C0-C3, in the order the study names them."""
    return [served_arm(condition) for condition in BASE_CONDITIONS]
