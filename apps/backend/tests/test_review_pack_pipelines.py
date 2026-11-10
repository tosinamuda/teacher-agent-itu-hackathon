"""Two pipeline versions of the revision pack, one stored specification injected into both.

2026-08-25 is the code Part 1's packs were generated with and must send exactly what it sent;
2026-09-02 is the code Part 2's personalised packs were generated with and must send what
that run sent. The specification
is data and is the same for both.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.experiments.domain.types import ConditionCode
from experiments.h1_condition_eval.fingerprints import material_digests
from scripts.prompt_snapshots import SERVED_DIR
from scripts.prompt_snapshots.render import served_snapshot_text, snapshot_name
from scripts.prompt_snapshots.served import served_arm

EVALUATED_DIR = Path("tests/snapshots/prompts/evaluated")
EVALUATED = EVALUATED_DIR / "2026-08-25" / "first-turn-messages.json"
STUDY_RUN = Path("experiments/h1_condition_eval/runs/c0c3-prism-objective")
BASE = (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3)
PACK = seed_specification(ArtefactType.POST_CLASS_REVIEW_PACK.value)


def test_the_latest_pipeline_is_2026_09_02() -> None:
    assert CURRENT_PIPELINE is ReviewPackPipeline.V2026_09_02


@pytest.mark.parametrize("condition", BASE, ids=lambda c: c.value)
def test_2026_08_25_sends_part_1s_first_turn_byte_for_byte(condition: ConditionCode) -> None:
    evaluated = json.loads(EVALUATED.read_text(encoding="utf-8"))[condition.value]

    arm = served_arm(condition, PACK, ReviewPackPipeline.V2026_08_25)

    assert arm.messages == evaluated


@pytest.mark.parametrize("condition", BASE, ids=lambda c: c.value)
def test_2026_09_02_sends_the_committed_first_turn(condition: ConditionCode) -> None:
    arm = served_arm(condition, PACK, ReviewPackPipeline.V2026_09_02)

    assert served_snapshot_text(arm) == (SERVED_DIR / snapshot_name(arm)).read_text()


def test_the_versions_differ_only_where_the_code_changed() -> None:
    """Same instructions and the same injected brief; only the tool list differs.

    The tool roster reaches the model in the user message, so that is where 2026-09-02's
    markdown note appears and the only place the two versions part.
    """
    first = served_arm(ConditionCode.C3, PACK, ReviewPackPipeline.V2026_08_25).messages
    second = served_arm(ConditionCode.C3, PACK, ReviewPackPipeline.V2026_09_02).messages
    requirement = PACK.requirements[0]

    assert first[0]["content"] == second[0]["content"]
    assert "never HTML" in second[1]["content"] and "never HTML" not in first[1]["content"]
    assert requirement in first[1]["content"] and requirement in second[1]["content"]


def test_2026_08_25_reproduces_every_prompt_input_part_1_fingerprinted() -> None:
    """Part 1's run recorded a digest of each prompt input; 2026-08-25 must match them all.

    ``arm.sampling`` is excluded: it is the decoding configuration, not prompt text.
    """
    arm = json.loads((STUDY_RUN / "run.json").read_text())["arm"]
    recorded = json.loads((STUDY_RUN / "fingerprint.json").read_text())["inputs"]
    reproduced = material_digests(
        arm["model"],
        arm["generator"],
        arm["repair"],
        arm["signatures"],
        arm["note_source"],
        arm["figures"],
        context_variant=arm["context_variant"],
        pipeline=ReviewPackPipeline.V2026_08_25,
    )

    differing = sorted(key for key in recorded if recorded[key] != reproduced.get(key))

    assert differing == ["arm.sampling"]


def test_a_pack_records_its_specification_revision_and_pipeline() -> None:
    from app.domains.artefacts.types.post_class_review_pack.application.grounding import Grounding
    from app.domains.artefacts.types.post_class_review_pack.application.student_pack_service import (  # noqa: E501
        StudentPackGenerationService,
    )
    from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import (
        ExpertSources,
    )

    service = StudentPackGenerationService(
        base_generator=object(),  # type: ignore[arg-type]
        learner_personaliser=object(),  # type: ignore[arg-type]
        lesson_notes=object(),  # type: ignore[arg-type]
        pipeline=ReviewPackPipeline.V2026_08_25,
    )

    assert service._provenance(PACK, Grounding(ExpertSources.TEXTBOOK, None)) == {
        "specification": {"kind": "post_class_review_pack", "revision": 1},
        "pipeline": "2026-08-25",
        "expert_sources": "textbook",
        "lesson_note": None,
    }


def test_the_content_route_takes_the_pipeline_version() -> None:
    from app.domains.content.api.schemas import GenerateContentRequest

    assert "pipeline" in GenerateContentRequest.model_fields


def test_the_pipelines_render_without_a_model() -> None:
    """Rendering only ever records; it never reaches a provider."""
    arms = asyncio.run(asyncio.to_thread(lambda: served_arm(ConditionCode.C0)))
    assert arms.messages


@pytest.mark.asyncio
async def test_2026_08_25_with_the_stored_spec_sends_part_1s_first_turn(db) -> None:
    """The app's path: the pack specification read from the database, injected into 2026-08-25."""
    from app.domains.artefacts.core.infrastructure.specifications import (
        SqlAlchemyContentSpecifications,
    )
    from migrations.data.content_registry_seed import seed_content_specifications

    connection = await db.connection()
    await connection.run_sync(seed_content_specifications)
    stored = await SqlAlchemyContentSpecifications().current(
        db, ArtefactType.POST_CLASS_REVIEW_PACK
    )
    evaluated = json.loads(EVALUATED.read_text(encoding="utf-8"))

    for condition in BASE:
        arm = await asyncio.to_thread(served_arm, condition, stored, ReviewPackPipeline.V2026_08_25)
        assert arm.messages == evaluated[condition.value], condition.value


def test_2026_08_25_validation_sends_part_1s_critic_and_repair_calls() -> None:
    from scripts.prompt_snapshots.finalise import critic_and_repair_messages

    recorded = json.loads((EVALUATED_DIR / "2026-08-25" / "critic-and-repair.json").read_text())

    assert critic_and_repair_messages(ReviewPackPipeline.V2026_08_25) == recorded


def test_2026_09_02_validation_sends_part_2s_critic_and_repair_calls() -> None:
    from scripts.prompt_snapshots.finalise import critic_and_repair_messages

    recorded = json.loads((EVALUATED_DIR / "2026-09-02" / "critic-and-repair.json").read_text())

    assert critic_and_repair_messages(ReviewPackPipeline.V2026_09_02) == recorded


def test_p1_sends_part_2s_personalisation_call() -> None:
    from scripts.prompt_snapshots.arms import personalisation_arm

    recorded = json.loads((EVALUATED_DIR / "2026-09-02" / "personalise-messages.json").read_text())
    arm = personalisation_arm(ConditionCode.P1)

    assert arm.call is not None
    assert arm.call.messages() == recorded["P1"]
