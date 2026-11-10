"""H2 personalises the first draw's C3 pack, approved once its validation has run — not C4."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.experiments.application.h2_base_pack import (
    H2_BASE_PACK_ID_PREFIX,
    approved_h2_base,
    first_draw_c3_artefact,
)
from app.domains.experiments.domain.types import ConditionedInputsMissingError

_START = datetime(2026, 8, 25, tzinfo=timezone.utc)
_MANIFEST = {
    "artefact_id": "AT-x",
    "scope": "class_level",
    "plan_version_id": "LPV-H2",
    "created_at": _START.isoformat(),
    "steps": [
        {
            "step_id": "s1",
            "lesson_objective_id": "lop01",
            "title": "Volume",
            "blocks": [{"type": "explanation", "id": "s1:b0", "content": "V = l x b x h"}],
        }
    ],
}


def _pack(artefact_id: str, status: ArtefactReviewStatus) -> SimpleNamespace:
    return SimpleNamespace(artefact_id=artefact_id, review_status=status, manifest=_MANIFEST)


@dataclass
class _Study:
    """One experiment's H1 draws, listed newest first as the repository returns them."""

    executions: list[SimpleNamespace] = field(default_factory=list)
    runs: dict[uuid.UUID, list[SimpleNamespace]] = field(default_factory=dict)
    packs: dict[str, SimpleNamespace] = field(default_factory=dict)

    def draw(self, number: int, **packs: SimpleNamespace) -> None:
        execution = SimpleNamespace(
            id=uuid.uuid4(),
            hypothesis="H1",
            attempt_number=number,
            created_at=_START + timedelta(days=number),
        )
        self.executions.insert(0, execution)
        self.runs[execution.id] = []
        for condition, pack in packs.items():
            run_id = f"ECR-d{number}-{condition}"
            self.runs[execution.id].append(
                SimpleNamespace(condition_code=condition, experiment_condition_run_id=run_id)
            )
            self.packs[run_id] = pack

    async def list_executions_for_experiment(self, _id: uuid.UUID) -> list[SimpleNamespace]:
        return self.executions

    async def list_condition_runs(self, execution_id: uuid.UUID) -> list[SimpleNamespace]:
        return self.runs[execution_id]

    async def current_artefact_for_condition_run(self, run_id: str) -> SimpleNamespace | None:
        return self.packs.get(run_id)


_EXPERIMENT = SimpleNamespace(id=uuid.uuid4())


@pytest.mark.asyncio
async def test_h2_reads_the_first_draws_approved_c3_pack_and_not_c4() -> None:
    study = _Study()
    study.draw(
        1,
        C3=_pack("AT-c3-d1", ArtefactReviewStatus.APPROVED),
        C4=_pack("AT-c4-d1", ArtefactReviewStatus.PENDING),
    )
    study.draw(2, C3=_pack("AT-c3-d2", ArtefactReviewStatus.APPROVED))
    study.draw(3, C3=_pack("AT-c3-d3", ArtefactReviewStatus.APPROVED))

    base = await approved_h2_base(experiments=study, experiment=_EXPERIMENT)  # type: ignore[arg-type]

    assert base.pack_id == f"{H2_BASE_PACK_ID_PREFIX}AT-c3-d1"
    assert [section.lesson_objective_id for section in base.sections] == ["lop01"]


@pytest.mark.asyncio
async def test_an_attempt_that_ran_no_c3_is_not_the_first_draw() -> None:
    study = _Study()
    study.draw(1)
    study.draw(2, C3=_pack("AT-c3-d2", ArtefactReviewStatus.APPROVED))

    pack = await first_draw_c3_artefact(experiments=study, experiment=_EXPERIMENT)  # type: ignore[arg-type]

    assert pack is not None and pack.artefact_id == "AT-c3-d2"


@pytest.mark.asyncio
async def test_h2_refuses_a_first_draw_c3_pack_that_is_not_approved() -> None:
    study = _Study()
    study.draw(1, C3=_pack("AT-c3-d1", ArtefactReviewStatus.PENDING))
    study.draw(2, C3=_pack("AT-c3-d2", ArtefactReviewStatus.APPROVED))

    with pytest.raises(ConditionedInputsMissingError, match="h2_requires_approved_c3_base"):
        await approved_h2_base(experiments=study, experiment=_EXPERIMENT)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_h2_has_no_base_before_h1_has_run() -> None:
    with pytest.raises(ConditionedInputsMissingError, match="h2_requires_first_draw_c3_base"):
        await approved_h2_base(experiments=_Study(), experiment=_EXPERIMENT)  # type: ignore[arg-type]
