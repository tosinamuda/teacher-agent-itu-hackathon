"""Each condition must get the orchestration its profile declares, and no other's.

Whether a pack is validated, whether a failure is repaired, and what the repair
and personalisation passes are allowed to see are declared on the profile;
the split generation entrypoints turn those declarations into calls.
The request-level suites prove the profile shapes the request — these prove the
service still consults the profile at all, so a gate that stops being read fails
here instead of silently equalising two conditions.

Driven with the shared stand-in model, so no LLM and no DB are involved.
"""

from __future__ import annotations

import random
from typing import cast

import pytest
from condition_leakage_support import (
    EchoModel,
    SilentCritic,
    build_canary_plan,
    stand_in_collaborators,
)

from app.domains.artefacts.types.post_class_review_pack.application.generate_base import (
    GenerateBaseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.personalise import (
    PersonaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.personalised.builder import (  # noqa: E501
    PersonalisedReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.section_generation import (
    SectionReviser,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    CheckResult,
    ReviewPackStructuralValidator,
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    assemble_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    section_cited_refs,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
    build_review_pack_personaliser,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.session_plan_view import SessionPlanView

H1_CODES = (
    ConditionCode.C0,
    ConditionCode.C1,
    ConditionCode.C2,
    ConditionCode.C3,
    ConditionCode.C4,
)
H2_CODES = (ConditionCode.P0, ConditionCode.P1)


class _RecordingValidator(ReviewPackStructuralValidator):
    """The real validator, counting how often the service reaches it."""

    def __init__(self) -> None:
        super().__init__()
        self.calls = 0

    def validate(
        self,
        *,
        policy: ReviewPackGenerationPolicy,
        sections: list[ReviewPackSection],
        request: ReviewPackRequest,
        base_sections: list[ReviewPackSection] | None = None,
    ) -> ValidationResult:
        self.calls += 1
        return super().validate(
            policy=policy, sections=sections, request=request, base_sections=base_sections
        )


class _UnitRecordingModel(EchoModel):
    """Stand-in model that also keeps the unit each pass was handed."""

    def __init__(self) -> None:
        super().__init__()
        self.repair_units: list[SectionGenerationUnit] = []
        self.personalise_units: list[SectionGenerationUnit] = []

    async def repair_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        failed_section: ReviewPackSection,
        issues: list[str],
    ) -> ReviewPackSection:
        self.repair_units.append(unit)
        return await super().repair_section(
            request=request, unit=unit, failed_section=failed_section, issues=issues
        )

    async def personalise_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection:
        self.personalise_units.append(unit)
        return await super().personalise_section(
            request=request, unit=unit, base_section=base_section, learner_state=learner_state
        )


def _condition_packs(
    *, model: EchoModel | None = None, validator: ReviewPackStructuralValidator | None = None
) -> GenerateBaseReviewPack:
    """The H1 pack maker over a deterministic model and the real validator."""
    return build_base_review_pack_generator(
        stand_in_collaborators(model or EchoModel()),
        validator=validator or ReviewPackStructuralValidator(),
    )


def _learner_packs(
    *, model: EchoModel | None = None, validator: ReviewPackStructuralValidator | None = None
) -> PersonaliseReviewPack:
    """The H2 pack maker over a deterministic model and the real validator."""
    return build_review_pack_personaliser(
        stand_in_collaborators(model or EchoModel()),
        validator=validator or ReviewPackStructuralValidator(),
    )


def _revision(
    model: EchoModel,
    *,
    reviser: SectionReviser | None = None,
) -> FinaliseReviewPack:
    return FinaliseReviewPack(
        generator=model,
        repairer=model,
        critic=SilentCritic(),
        reviser=reviser,
    )


def _plan() -> SessionPlanView:
    return build_canary_plan(random.Random(20260810)).view


def _multi_reference_plan() -> SessionPlanView:
    """A plan carrying several references, so evidence scoping has something to cut."""
    return SessionPlanView.model_validate(
        {
            "subject": "Mathematics",
            "grade": "JSS1",
            "topic": "Area of plane shapes",
            "lesson_plan_objectives": [
                {"lesson_objective_id": "lop01", "objective_text": "Find the area of rectangles."}
            ],
            "references": [
                "Textbook p.42: area = length x width",
                "Textbook p.43: worked example",
                "Textbook p.44: exercises",
            ],
            "steps": [
                {
                    "step_id": "s1",
                    "step_kind": "core",
                    "lesson_objective_id": "lop01",
                    "title": "Rectangle area",
                    "content": "Area equals length times width.",
                }
            ],
        }
    )


def _learner_state(objective_id: str) -> ObjectiveLearnerState:
    return ObjectiveLearnerState(
        lesson_objective_id=objective_id, mastery_band="remediate", mastery="0 of 2 correct"
    )


def _base_section(objective_id: str, refs: list[str]) -> ReviewPackSection:
    return ReviewPackSection(
        section_id=f"objective:{objective_id}",
        title="Approved base section",
        lesson_objective_id=objective_id,
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="Multiply the two side lengths.",
                lesson_objective_id=objective_id,
                source_refs=refs,
            )
        ],
        source_refs=refs,
    )


class _SilentPersonaliser(EchoModel):
    """A personaliser that writes nothing — the failure the base fallback is for."""

    async def personalise_section(self, **kwargs: object) -> ReviewPackSection:
        unit = cast(SectionGenerationUnit, kwargs["unit"])
        return assemble_section(title="", blocks=[], practice=[], unit=unit)


class _PassingValidator(ReviewPackStructuralValidator):
    """Validation off, so the fallback is what the assertions see.

    P1 validates and repairs, and repair writes prose of its own — enough to
    hide an empty personalisation behind a section that looks fine.
    """

    def validate(self, **kwargs: object) -> ValidationResult:
        return ValidationResult(passed=True, checks=[])


@pytest.mark.asyncio
async def test_a_personaliser_that_writes_nothing_falls_back_to_the_approved_base() -> None:
    """A figure is not content, and the guard could not tell the difference.

    The unit's grounded figures are spliced in after generation, so a section
    whose model returned nothing still arrives with a non-empty block list.
    Testing that list shipped an image and no words as the personalised section
    — and only where figures travel, which is the grounded half of H2.
    """
    plan = _plan()
    objective_id = plan.lesson_plan_objectives[0].lesson_objective_id
    base = _base_section(objective_id, ["REF-1"])
    personaliser = _learner_packs(model=_SilentPersonaliser(), validator=_PassingValidator())
    result = await personaliser.personalise(
        session_plan=plan,
        base_sections=[base],
        learner_states={objective_id: _learner_state(objective_id)},
        base_pack_id="AT-base",
        focal_learner_id="STU-1",
        policy=profile_for(Hypothesis.H2, ConditionCode.P1),
        sources=LessonSources.unresolved(plan.references),
    )
    assert [section.title for section in result.sections] == [base.title]
    assert any(block.text for block in result.sections[0].blocks), (
        "the personalised section carries no prose at all"
    )


def _failing_validation(objective_id: str) -> ValidationResult:
    """A failure attributed to one section, so ``_repair`` targets exactly it."""
    return ValidationResult(
        passed=False,
        checks=[
            CheckResult(
                check="scope_compliance",
                passed=False,
                message=f"{objective_id}: section leaves the approved scope",
                details={"out_of_scope": [objective_id]},
            )
        ],
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("code", H1_CODES)
async def test_only_validated_h1_conditions_reach_the_validator(code: ConditionCode) -> None:
    """An unvalidated condition must not acquire its validated sibling's pass.

    Deleting the gate — rather than inverting it — would run C3's validate and
    repair loop for C0/C1/C2 as well, collapsing the C2/C3 contrast into nothing
    while every request-level assertion still passed.
    """
    profile = profile_for(Hypothesis.H1, code)
    plan = _plan()
    validator = _RecordingValidator()
    result = await _condition_packs(validator=validator).generate(
        session_plan=plan,
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    if profile.validation.enabled:
        assert validator.calls >= 1
        assert result.validation is not None
    else:
        assert validator.calls == 0
        assert result.validation is None
        assert result.repaired is False


@pytest.mark.asyncio
@pytest.mark.parametrize("code", H2_CODES)
async def test_only_validated_h2_conditions_reach_the_validator(code: ConditionCode) -> None:
    profile = profile_for(Hypothesis.H2, code)
    plan = _plan()
    objective_id = plan.lesson_plan_objectives[0].lesson_objective_id
    validator = _RecordingValidator()
    result = await _learner_packs(validator=validator).personalise(
        session_plan=plan,
        base_sections=[_base_section(objective_id, ["REF-1"])],
        learner_states={objective_id: _learner_state(objective_id)},
        base_pack_id="AT-base",
        focal_learner_id="STU-1",
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    if profile.validation.enabled:
        assert validator.calls >= 1
        assert result.validation is not None
    else:
        assert validator.calls == 0
        assert result.validation is None
        assert result.repaired is False


@pytest.mark.asyncio
async def test_p1_repair_is_handed_a_unit_with_no_lesson_plan_prose() -> None:
    """The H2 rule — adapt the approved base, never regenerate from the plan.

    ``_unit_for_personalisation_repair`` strips the step fields; this proves the repair pass
    actually calls it, which is the half that has no other coverage.
    """
    plan = _plan()
    profile = profile_for(Hypothesis.H2, ConditionCode.P1)
    model = _UnitRecordingModel()
    revision = _revision(model)
    request = PersonalisedReviewPackRequestBuilder().build(
        session_plan=plan,
        base_pack_id="AT-base",
        focal_learner_id="STU-1",
        learner_states={},
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    unit = request.units[0]
    assert unit.student_tasks or unit.instructional_events, (
        "the fixture must carry plan context for the strip to be provable"
    )
    section = _base_section(unit.lesson_objective_id, ["REF-1"])
    section.section_id = unit.unit_id

    await revision._revise(
        policy=profile,
        request=request,
        sections=[section],
        validation=_failing_validation(unit.lesson_objective_id),
        base_sections=[section],
    )

    assert len(model.repair_units) == 1
    repaired = model.repair_units[0]
    assert repaired.step_content is None
    assert repaired.step_title is None
    assert repaired.instructional_type is None
    assert repaired.estimated_minutes is None
    # Position and step identity are plan context too: they say where in her
    # lesson this section sat, which personalisation never sees.
    assert repaired.current_step is None
    assert repaired.source_step_id is None
    assert repaired.activities == []
    assert repaired.instructional_events == []
    assert repaired.student_tasks == []
    assert repaired.assessment_points == []


@pytest.mark.asyncio
async def test_c3_repair_keeps_the_lesson_plan_step() -> None:
    """The strip is P1-only: C3 repairs against the plan it generated from."""
    plan = _plan()
    profile = profile_for(Hypothesis.H1, ConditionCode.C3)
    model = _UnitRecordingModel()
    revision = _revision(model)
    request = BaseReviewPackRequestBuilder().build(
        session_plan=plan,
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    unit = request.units[0]
    section = _base_section(unit.lesson_objective_id, ["REF-1"])
    section.section_id = unit.unit_id

    await revision._revise(
        policy=profile,
        request=request,
        sections=[section],
        validation=_failing_validation(unit.lesson_objective_id),
        base_sections=None,
    )

    assert len(model.repair_units) == 1
    assert model.repair_units[0].instructional_events == unit.instructional_events
    assert model.repair_units[0].student_tasks == unit.student_tasks


@pytest.mark.asyncio
async def test_p1_personalisation_sees_only_the_evidence_the_base_cites() -> None:
    """Personalisation adapts the approved base, so it may not re-open the rest.

    The unit carries every reference the plan resolved; only the excerpts the
    approved base section actually cites may reach the model.
    """
    plan = _multi_reference_plan()
    profile = profile_for(Hypothesis.H2, ConditionCode.P1)
    model = _UnitRecordingModel()
    personaliser = _learner_packs(model=model)
    objective_id = plan.lesson_plan_objectives[0].lesson_objective_id
    request = personaliser.build_request(
        session_plan=plan,
        base_pack_id="AT-base",
        focal_learner_id="STU-1",
        learner_states={},
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    carried = [item.source_ref for item in request.units[0].source_evidence]
    assert len(carried) > 1, "the fixture must carry several refs for scoping to be provable"

    await personaliser.personalise(
        session_plan=plan,
        base_sections=[_base_section(objective_id, [carried[0]])],
        learner_states={objective_id: _learner_state(objective_id)},
        base_pack_id="AT-base",
        focal_learner_id="STU-1",
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )

    assert len(model.personalise_units) == 1
    scoped = [item.source_ref for item in model.personalise_units[0].source_evidence]
    assert scoped == [carried[0]]


class _RecordingReviser:
    """A reviser that marks what it was asked to edit, and with which findings."""

    def __init__(self) -> None:
        self.seen: list[tuple[str, list[str]]] = []

    async def revise(self, *, section: ReviewPackSection, findings: list[str]) -> ReviewPackSection:
        self.seen.append((section.lesson_objective_id, findings))
        return section.model_copy(update={"title": f"edited:{section.lesson_objective_id}"})


@pytest.mark.asyncio
async def test_only_the_flagged_sections_are_handed_to_the_reviser() -> None:
    """The editing branch touches what validation implicated, and nothing else.

    Editing is span-local by design — a section nothing was said about must come
    back byte-identical, because a blind pass over a clean section is how repair
    collateral happens. This branch had no coverage at all until the reviser
    became an injectable seam.
    """
    reviser = _RecordingReviser()
    model = EchoModel()
    revision = _revision(model, reviser=reviser)
    profile = profile_for(Hypothesis.H1, ConditionCode.C3)
    plan = _plan()
    request = BaseReviewPackRequestBuilder().build(
        session_plan=plan,
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    flagged = _base_section("lop01", ["REF-1"])
    untouched = _base_section("lop02", ["REF-1"])

    revised = await revision._revise(
        policy=profile,
        request=request,
        sections=[flagged, untouched],
        validation=_failing_validation("lop01"),
        base_sections=None,
    )

    assert [objective for objective, _ in reviser.seen] == ["lop01"]
    assert revised[0].title == "edited:lop01"
    assert revised[1] is untouched
    # The findings routed to the section are its own, not the whole pack's.
    assert all("lop01" in finding for _, findings in reviser.seen for finding in findings)


@pytest.mark.asyncio
async def test_the_editing_branch_is_taken_only_when_a_reviser_is_injected() -> None:
    """Without one, a flagged pack goes through the whole-section repair instead."""
    reviser = _RecordingReviser()
    model = _UnitRecordingModel()
    plan = _plan()
    profile = profile_for(Hypothesis.H1, ConditionCode.C3)
    request = BaseReviewPackRequestBuilder().build(
        session_plan=plan,
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    section = _base_section(request.units[0].lesson_objective_id, ["REF-1"])
    section.section_id = request.units[0].unit_id
    validation = _failing_validation(section.lesson_objective_id)

    with_editing = _revision(model, reviser=reviser)
    await with_editing._revise(
        policy=profile,
        request=request,
        sections=[section],
        validation=validation,
        base_sections=None,
    )
    assert reviser.seen and model.repair_units == []

    reviser.seen.clear()
    await _revision(model)._revise(
        policy=profile,
        request=request,
        sections=[section],
        validation=validation,
        base_sections=None,
    )
    assert not reviser.seen and model.repair_units


def test_a_base_section_cites_through_prose_as_well_as_structure() -> None:
    """P1 scopes its evidence to what the approved base cites — both channels.

    A pack recovered from a stored manifest carries its refs only as the
    rendered "_Sources:" line, and the model writes the marker with a
    non-breaking hyphen (U+2011) often enough that a pattern keyed on the ASCII
    one stripped none of 25 markers in a real pack. Reading structure alone
    would scope P1's evidence to nothing and hand it the whole reference list.
    """
    structured = _base_section("lop01", ["REF-1"])
    assert section_cited_refs(structured) == {"REF-1"}

    inline = _base_section("lop01", [])
    inline.blocks[0].text = "Multiply the sides.\n\n_Sources: REF-2_"
    assert section_cited_refs(inline) == {"REF-2"}

    non_breaking = _base_section("lop01", [])
    non_breaking.blocks[0].text = "Multiply the sides.\n\n_Sources: REF‑3_"
    assert section_cited_refs(non_breaking) == {"REF-3"}, (
        "a ref written with a non-breaking hyphen must normalise to the issued form"
    )

    assert section_cited_refs(_base_section("lop01", [])) == set()
