"""The first critic call and first repair call a pack's validation makes, per pipeline.

Both are recorded from the modules production builds, over a model that keeps the first
request and refuses it, for C3's first unit and the fixture's base section.
"""

from __future__ import annotations

import asyncio

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import ReviewPackPipeline
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    section_collaborators,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from scripts.prompt_snapshots import fixture
from scripts.prompt_snapshots.served import _RecordingLM

REPAIR_ISSUE = "The worked example skips a step."


def _first(lm: _RecordingLM, call: object) -> list[dict[str, str]]:
    try:
        asyncio.run(call)  # type: ignore[arg-type]
    except Exception:  # noqa: BLE001 - the recorder refuses every call once it has one
        pass
    if lm.first is None:
        raise AssertionError("the module finished without calling the model")
    return lm.first


def critic_and_repair_messages(pipeline: ReviewPackPipeline) -> dict[str, list[dict[str, str]]]:
    """The critic's and the repairer's first request under one pipeline version."""
    profile = profile_for(Hypothesis.H1, ConditionCode.C3)
    request = BaseReviewPackRequestBuilder().build(
        session_plan=fixture.SESSION_PLAN,
        policy=profile.generation_policy(),
        sources=fixture.LESSON_SOURCES,
    )
    unit = next(
        u
        for u in request.units
        if u.lesson_objective_id == fixture.BASE_SECTION.lesson_objective_id
    )
    critic_lm, repair_lm = _RecordingLM(), _RecordingLM()
    critic = section_collaborators(critic_lm, pipeline).critic
    repairer = section_collaborators(repair_lm, pipeline).repairer
    return {
        "critic": _first(
            critic_lm,
            critic.review(
                request=request,
                sections=[fixture.BASE_SECTION],
                checks=profile.validation.checks,
            ),
        ),
        "repair": _first(
            repair_lm,
            repairer.repair_section(
                request=request,
                unit=unit,
                failed_section=fixture.BASE_SECTION,
                issues=[REPAIR_ISSUE],
            ),
        ),
    }
