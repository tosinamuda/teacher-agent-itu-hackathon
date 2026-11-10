"""Condition leakage DOWNSTREAM of generation (H1 C0-C4, H2 P1).

A sibling suite proves that a condition's forbidden lesson-plan context never
reaches the generation request or the prompt. That guarantee is worth nothing if
the context re-enters afterwards, so this suite audits the rest of the chain:

    generated section -> normalise_section / _append_grounded_figures
                      -> generated_pack_record           (ExperimentConditionRun.generated_pack)
                      -> review_pack_manifest   (Artefact.manifest — what raters read)
                      -> flat rating rows       (the analysis dataset)

Every plan field carries a canary tagged with the class of context it belongs to
(see ``tests.condition_leakage_support``), the model is an adversarial echo that
regurgitates its whole input and invents a textbook figure, and each condition's
final rater-visible JSON is asserted to contain ONLY the classes that condition
allows. Cross-run contamination lives in ``test_condition_run_isolation``.
"""

from __future__ import annotations

import random
from datetime import datetime, timezone

import pytest

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.condition_run_artefact import (  # noqa: E501  # noqa: E501
    review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
    build_review_pack_personaliser,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.evaluation.application.export_schemas import H1RatingRow, H2RatingRow
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.infrastructure.generated_review_pack_record import (
    generated_pack_record,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from tests.condition_leakage_support import (
    DESIGN,
    EVIDENCE,
    FIGURE,
    GLOBAL,
    OBJECTIVE,
    PLAN_ONLY,
    ROGUE,
    ROGUE_FIGURE_URL,
    STEP,
    CanaryPlan,
    EchoModel,
    build_canary_plan,
    classes_in,
    fuzz_seeds,
    stand_in_collaborators,
)

_CREATED_AT = datetime(2026, 8, 10, tzinfo=timezone.utc)

# What each H1 condition is allowed to surface in its rater-visible pack.
# PLAN_ONLY and ROGUE appear in no set: no condition may surface a plan field
# its request never carried, or a figure the model invented.
_ALLOWED: dict[ConditionCode, set[str]] = {
    ConditionCode.C0: {OBJECTIVE, GLOBAL},
    # C1 and up receive the plan's instructional guidance: the step they write
    # from, and the ordered outline it sits in.
    ConditionCode.C1: {OBJECTIVE, GLOBAL, STEP, DESIGN},
    ConditionCode.C2: {OBJECTIVE, GLOBAL, STEP, DESIGN, EVIDENCE, FIGURE},
    ConditionCode.C3: {OBJECTIVE, GLOBAL, STEP, DESIGN, EVIDENCE, FIGURE},
    # C4 forks C3's generation, so it inherits exactly C3's allowance.
    ConditionCode.C4: {OBJECTIVE, GLOBAL, STEP, DESIGN, EVIDENCE, FIGURE},
}
_GROUNDED = (ConditionCode.C2, ConditionCode.C3, ConditionCode.C4)


async def _run_condition(
    plan: CanaryPlan, code: ConditionCode, *, model: EchoModel | None = None
) -> tuple[dict, dict, EchoModel]:
    """Generate + project one H1 condition exactly as the runner persists it."""
    echo = model or EchoModel()
    generator = build_base_review_pack_generator(stand_in_collaborators(echo))
    # A forked condition (C4) never generates: it persists its source's result.
    profile = profile_for(Hypothesis.H1, code)
    source = profile_for(Hypothesis.H1, profile.generated_by)
    result = await generator.generate(
        session_plan=plan.view,
        policy=source,
        sources=plan.sources,
    )
    manifest = review_pack_manifest(
        result,
        artefact_id=f"AT-{code.value}",
        plan_version_id="LPV-1",
        scope=ArtefactScope.CLASS_LEVEL,
        student_id=None,
        created_at=_CREATED_AT,
    )
    return generated_pack_record(result), manifest, echo


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(1, 7, 13, 29, 101, 997))
@pytest.mark.parametrize("code", list(_ALLOWED))
async def test_condition_pack_carries_only_its_allowed_context(
    seed: int, code: ConditionCode
) -> None:
    plan = build_canary_plan(random.Random(seed))
    payload, manifest, _ = await _run_condition(plan, code)

    for name, projection in (("generated_pack", payload), ("manifest", manifest)):
        leaked = classes_in(projection) - _ALLOWED[code]
        assert not leaked, f"{code.value} {name} leaked context classes {sorted(leaked)}"

    # Positive controls — without these the assertion above passes vacuously.
    found = classes_in(manifest)
    assert OBJECTIVE in found and GLOBAL in found
    assert (STEP in found) is (code is not ConditionCode.C0)
    assert (EVIDENCE in found) is (code in _GROUNDED)
    # Plan fields no request ever carries, and figures the model invented.
    assert PLAN_ONLY not in found and ROGUE not in found


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(3, 17, 61))
async def test_c3_repair_pass_does_not_widen_the_allowed_context(seed: int) -> None:
    """A validation failure re-enters generation — the repair must stay in-condition."""
    plan = build_canary_plan(random.Random(seed))
    echo = EchoModel(bad_refs_first_call=True)
    payload, manifest, used = await _run_condition(plan, ConditionCode.C3, model=echo)

    assert used.repaired, "the repair pass never ran — the test proves nothing"
    for projection in (payload, manifest):
        assert not classes_in(projection) - _ALLOWED[ConditionCode.C3]
    assert _visual_urls(manifest) == list(plan.figure_urls)


# ===== Figure gate =====


def _visual_urls(manifest: dict) -> list[str]:
    return [
        block["url"]
        for step in manifest["steps"]
        for block in step["blocks"]
        if block.get("type") == "visual"
    ]


def _sections_from(payload: dict) -> list[ReviewPackSection]:
    return [ReviewPackSection.model_validate(raw) for raw in payload["sections"]]


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(2, 23, 89))
@pytest.mark.parametrize("code", list(_ALLOWED))
async def test_figure_gate_holds_when_the_model_authors_its_own_visual(
    seed: int, code: ConditionCode
) -> None:
    """Model-authored visuals are dropped; only the plan's grounded figures land.

    This is the path by which a C0/C1 pack could otherwise acquire a textbook
    figure — the echo model emits a ``visual`` block on every section.
    """
    plan = build_canary_plan(random.Random(seed))
    _, manifest, _ = await _run_condition(plan, code)

    expected = list(plan.figure_urls) if code in _GROUNDED else []
    assert _visual_urls(manifest) == expected
    assert ROGUE_FIGURE_URL not in str(manifest)
    assert ROGUE not in classes_in(manifest)


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(5, 41))
async def test_p1_pack_carries_learner_state_but_no_extra_plan_context(seed: int) -> None:
    """P1 adapts an approved base; the lesson plan must not re-enter through it."""
    plan = build_canary_plan(random.Random(seed))
    base_payload, base_manifest, _ = await _run_condition(plan, ConditionCode.C3)
    base_sections = _sections_from(base_payload)
    objective_ids = sorted({section.lesson_objective_id for section in base_sections})
    echo = EchoModel(marker="p1-marker")
    personaliser = build_review_pack_personaliser(stand_in_collaborators(echo))
    result = await personaliser.personalise(
        session_plan=plan.view,
        base_sections=base_sections,
        learner_states={
            objective_id: ObjectiveLearnerState(
                lesson_objective_id=objective_id, mastery_band="remediate"
            )
            for objective_id in objective_ids
        },
        base_pack_id="AT-C3",
        focal_learner_id="STU-1",
        policy=profile_for(Hypothesis.H2, ConditionCode.P1),
        sources=plan.sources,
    )
    manifest = review_pack_manifest(
        result,
        artefact_id="AT-P1",
        plan_version_id="LPV-1",
        scope=ArtefactScope.LEARNER_LEVEL,
        student_id="STU-1",
        created_at=_CREATED_AT,
    )

    assert echo.personalised, "the personaliser never ran"
    # P1 inherits C3's allowance (it personalises C3's approved pack) and adds
    # nothing: the base pack already carried step context, so STEP is expected.
    assert not classes_in(manifest) - _ALLOWED[ConditionCode.C3]
    assert _visual_urls(manifest) == list(plan.figure_urls)
    # Section identity survives personalisation — the H2 rater view pairs base and
    # candidate steps by step_id, so a collapsed or renamed id mispairs the packet.
    assert [step["step_id"] for step in manifest["steps"]] == [
        step["step_id"] for step in base_manifest["steps"]
    ]


# ===== Analysis dataset =====


def test_dataset_export_rows_carry_no_pack_content() -> None:
    """A C0 row cannot carry C1+ material because no export column holds pack text.

    Pinning the column sets makes adding a pack/plan-derived column to the
    analysis dataset a deliberate, test-breaking act rather than a silent one.
    """
    scores_and_ids = {
        "experiment_id",
        "lesson_id",
        "condition_code",
        "packet_id",
        "rater_id",
        "synthetic",
        "focal_learner_id",
        "section_id",
    }
    for row_model in (H1RatingRow, H2RatingRow):
        text_columns = {
            name
            for name, info in row_model.model_fields.items()
            if name not in scores_and_ids and _may_hold_text(info.annotation)
        }
        assert text_columns <= {"major_issues", "major_issue_other"}, (
            f"{row_model.__name__} gained a free-text column: {sorted(text_columns)}"
        )


def _may_hold_text(annotation: object) -> bool:
    return "str" in str(annotation)


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(5, 41, 907))
async def test_p1_built_from_a_manifest_recovered_base_leaks_nothing_new(seed: int) -> None:
    """H2 starts from a manifest, not from a generation result.

    Production recovers the approved base pack out of the stored artefact
    (``c4_base_pack``), so a leak introduced by that recovery — or a
    context class silently gained or dropped crossing the manifest boundary —
    is invisible to a test that hands ``personalise`` the raw sections. This
    drives the real recovery.
    """
    plan = build_canary_plan(random.Random(seed))
    base_payload, base_manifest, _ = await _run_condition(plan, ConditionCode.C3)
    recovered = review_pack_manifest_to_sections(PostClassReviewPack.model_validate(base_manifest))

    # The boundary must neither lose nor invent context.
    assert classes_in([section.model_dump(mode="json") for section in recovered]) == classes_in(
        base_payload["sections"]
    )
    # And the refs must survive as structure, not only as prose.
    assert any(block.source_refs for section in recovered for block in section.blocks)

    objective_ids = sorted({section.lesson_objective_id for section in recovered})
    echo = EchoModel(marker="p1-from-manifest")
    personaliser = build_review_pack_personaliser(stand_in_collaborators(echo))
    result = await personaliser.personalise(
        session_plan=plan.view,
        base_sections=recovered,
        learner_states={
            objective_id: ObjectiveLearnerState(
                lesson_objective_id=objective_id, mastery_band="remediate"
            )
            for objective_id in objective_ids
        },
        base_pack_id="AT-C3",
        focal_learner_id="STU-1",
        policy=profile_for(Hypothesis.H2, ConditionCode.P1),
        sources=plan.sources,
    )
    manifest = review_pack_manifest(
        result,
        artefact_id="AT-P1",
        plan_version_id="LPV-1",
        scope=ArtefactScope.LEARNER_LEVEL,
        created_at=_CREATED_AT,
        student_id="STU-1",
    )
    assert not classes_in(manifest) - _ALLOWED[ConditionCode.C3]
    assert PLAN_ONLY not in classes_in(manifest) and ROGUE not in classes_in(manifest)
    # Re-rendering a recovered pack must not stack a second attribution line.
    for step in manifest["steps"]:
        for block in step["blocks"]:
            assert str(block.get("content", "")).count("_Sources:") <= 1
