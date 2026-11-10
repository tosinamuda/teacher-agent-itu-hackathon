"""H2 evaluation-section pairing: base-pack iteration + `candidate_missing`.

Per the Evaluation Protocol §4, H2 rating sections are built from the BASE pack so
a personalised section the candidate drops is surfaced (not silently skipped) and
penalised under objective preservation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import cast

import pytest

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.schemas import (
    PostClassReviewPack,
    ReviewPackStep,
)
from app.domains.evaluation.application.peer_ports import PackArtefactsPort
from app.domains.evaluation.application.rating_validation import RatingValidationService
from app.shared.session_plan_view import SessionPlanView
from tests.evaluation_collaborators import NoPackArtefacts


@dataclass(frozen=True)
class _Runtime:
    session_plan: SessionPlanView


def _pack(steps: list[ReviewPackStep]) -> PostClassReviewPack:
    return PostClassReviewPack(
        artefact_id="AT-test",
        scope=ArtefactScope.LEARNER_LEVEL,
        plan_version_id="LPV-test",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        steps=steps,
    )


@pytest.mark.asyncio
async def test_h2_sections_iterate_base_and_flag_candidate_missing() -> None:
    """A base section the personalised candidate drops is surfaced and flagged."""
    validation = RatingValidationService(cast(PackArtefactsPort, NoPackArtefacts()))
    base = _pack(
        [
            ReviewPackStep(step_id="step:step01", title="Multiples", lesson_objective_id="lop01"),
            ReviewPackStep(step_id="step:step02", title="LCM", lesson_objective_id="lop02"),
        ]
    )
    candidate = _pack(
        [
            ReviewPackStep(
                step_id="step:step01",
                title="Common multiples (eased)",
                lesson_objective_id="lop01",
            )
        ]
    )
    # source_artefact_plan_id=None short-circuits the plan lookup.
    artefact = Artefact(source_artefact_plan_id=None)
    runtime = _Runtime(session_plan=SessionPlanView.model_validate({}))

    sections = await validation.h2_section_payloads(
        runtime=runtime,
        base_artefact=artefact,
        base_manifest=base,
        candidate_artefact=artefact,
        candidate_manifest=candidate,
    )

    # Sections come from the base pack, in base order.
    assert [s["section_id"] for s in sections] == ["step:step01", "step:step02"]
    # Present section: paired with its candidate, not flagged.
    assert sections[0]["candidate_missing"] is False
    assert sections[0]["candidate_step"] is not None
    # Dropped section: still surfaced (from the base pack) and flagged for the rater.
    assert sections[1]["candidate_missing"] is True
    assert sections[1]["candidate_step"] is None
    assert sections[1]["base_step"] is not None
