"""What a personalised pack records about its own personalisation.

P1 keeps the approved base section in two cases — the learner has no state for
that objective, and the model answers with nothing a learner can read. Both leave
a pack whose prose cannot be told apart from one the model adapted, in the arm
whose entire measurement is personalisation. These tests pin the record that
makes the difference visible to analysis.
"""

from __future__ import annotations

import random

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    PERSONALISED_REVIEW_PACK_POLICY,
    ReviewPackGenerationPolicy,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.personalisation import (
    PersonalisationOutcome,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
    build_review_pack_personaliser,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.infrastructure.generated_review_pack_record import (
    generated_pack_record,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from tests.condition_leakage_support import (
    CanaryPlan,
    EchoModel,
    build_canary_plan,
    stand_in_collaborators,
)


class _SilentOnOneSection(EchoModel):
    """A personaliser that answers one section with visuals and nothing else.

    The real failure this stands in for: a model that returns a section whose
    only blocks are figures, which carries no teaching at all.
    """

    def __init__(self, *, silent_section_id: str) -> None:
        super().__init__()
        self.silent_section_id = silent_section_id

    async def personalise_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection:
        section = await super().personalise_section(
            request=request,
            unit=unit,
            base_section=base_section,
            learner_state=learner_state,
        )
        if base_section.section_id != self.silent_section_id:
            return section
        return section.model_copy(
            update={"blocks": [block for block in section.blocks if block.block_type == "visual"]}
        )


async def _base_sections(plan: CanaryPlan) -> list[ReviewPackSection]:
    """An approved C4-style base pack for P1 to personalise."""
    result = await build_base_review_pack_generator(stand_in_collaborators(EchoModel())).generate(
        session_plan=plan.view,
        policy=profile_for(Hypothesis.H1, ConditionCode.C3),
        sources=plan.sources,
    )
    return result.sections


async def _personalise(
    plan: CanaryPlan,
    base_sections: list[ReviewPackSection],
    *,
    model: EchoModel,
    learner_states: dict[str, ObjectiveLearnerState],
    policy: ReviewPackGenerationPolicy | None = None,
    marked_questions: dict[str, int] | None = None,
) -> GeneratedReviewPack:
    return await build_review_pack_personaliser(stand_in_collaborators(model)).personalise(
        session_plan=plan.view,
        base_sections=base_sections,
        learner_states=learner_states,
        base_pack_id="AT-C4",
        focal_learner_id="STU-A",
        policy=policy or profile_for(Hypothesis.H2, ConditionCode.P1),
        sources=plan.sources,
        marked_questions=marked_questions,
    )


def _states(sections: list[ReviewPackSection]) -> dict[str, ObjectiveLearnerState]:
    return {
        section.lesson_objective_id: ObjectiveLearnerState(
            lesson_objective_id=section.lesson_objective_id,
            mastery_band="remediate",
        )
        for section in sections
    }


@pytest.mark.asyncio
async def test_a_pack_records_which_sections_personalisation_actually_adapted() -> None:
    plan = build_canary_plan(random.Random(11))
    base_sections = await _base_sections(plan)
    assert len(base_sections) > 2, "the fixture needs a section per outcome"
    silent, unstated = base_sections[0], base_sections[-1]

    states = _states(base_sections)
    del states[unstated.lesson_objective_id]
    pack = await _personalise(
        plan,
        base_sections,
        model=_SilentOnOneSection(silent_section_id=silent.section_id),
        learner_states=states,
    )

    outcomes = {record.section_id: record.outcome for record in pack.personalisation}
    assert outcomes.pop(silent.section_id) == PersonalisationOutcome.EMPTY_RESULT
    assert outcomes.pop(unstated.section_id) == PersonalisationOutcome.NO_LEARNER_STATE
    assert set(outcomes.values()) == {PersonalisationOutcome.PERSONALISED}
    assert len(pack.personalisation) == len(base_sections)


@pytest.mark.asyncio
async def test_a_silent_fallback_keeps_the_base_prose_and_says_so() -> None:
    """The section is the base one verbatim, and the record is what shows it."""
    plan = build_canary_plan(random.Random(23))
    base_sections = await _base_sections(plan)
    silent = base_sections[0]
    base_prose = [block.text for block in silent.blocks if block.block_type != "visual"]

    pack = await _personalise(
        plan,
        base_sections,
        model=_SilentOnOneSection(silent_section_id=silent.section_id),
        learner_states=_states(base_sections),
    )

    kept = next(section for section in pack.sections if section.section_id == silent.section_id)
    assert [block.text for block in kept.blocks if block.block_type != "visual"] == base_prose


@pytest.mark.asyncio
async def test_the_personalisation_record_reaches_the_persisted_condition_run() -> None:
    """A record analysis cannot read back is no record at all."""
    plan = build_canary_plan(random.Random(37))
    base_sections = await _base_sections(plan)
    silent = base_sections[0]

    pack = await _personalise(
        plan,
        base_sections,
        model=_SilentOnOneSection(silent_section_id=silent.section_id),
        learner_states=_states(base_sections),
    )

    recorded = generated_pack_record(pack)["personalisation"]
    assert isinstance(recorded, list)
    assert {entry["outcome"] for entry in recorded} == {
        PersonalisationOutcome.EMPTY_RESULT.value,
        PersonalisationOutcome.PERSONALISED.value,
    }
    assert [entry["section_id"] for entry in recorded] == [
        section.section_id for section in base_sections
    ]


@pytest.mark.asyncio
async def test_a_section_stays_as_it_was_when_too_few_questions_were_marked_for_its_objective() -> (
    None
):
    plan = build_canary_plan(random.Random(11))
    base_sections = await _base_sections(plan)
    thin = base_sections[0]
    enough = next(s for s in base_sections if s.lesson_objective_id != thin.lesson_objective_id)
    marked = {section.lesson_objective_id: 3 for section in base_sections}
    marked[thin.lesson_objective_id] = 1

    pack = await _personalise(
        plan,
        base_sections,
        model=EchoModel(),
        learner_states=_states(base_sections),
        policy=PERSONALISED_REVIEW_PACK_POLICY,
        marked_questions=marked,
    )

    outcomes = {record.section_id: record.outcome for record in pack.personalisation}
    assert outcomes[thin.section_id] == PersonalisationOutcome.THIN_EVIDENCE
    assert outcomes[enough.section_id] == PersonalisationOutcome.PERSONALISED
    kept = next(s for s in pack.sections if s.section_id == thin.section_id)
    assert kept == thin


@pytest.mark.asyncio
async def test_a_policy_that_asks_for_no_minimum_adapts_on_any_evidence() -> None:
    plan = build_canary_plan(random.Random(11))
    base_sections = await _base_sections(plan)
    marked = {section.lesson_objective_id: 1 for section in base_sections}

    pack = await _personalise(
        plan,
        base_sections,
        model=EchoModel(),
        learner_states=_states(base_sections),
        marked_questions=marked,
    )

    assert {r.outcome for r in pack.personalisation} == {PersonalisationOutcome.PERSONALISED}
