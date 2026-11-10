"""FD-03: derive distractor→misconception tags (pure filter + service, LLM mocked)."""

from __future__ import annotations

import pytest

from app.domains.assessments.application.classwork_service import ClassworkApplicationService
from app.domains.assessments.application.misconception_deriver import (
    MisconceptionDeriver,
    valid_misconceptions,
)
from app.domains.assessments.classwork_schemas import DeriveMisconceptionsItem


def test_valid_misconceptions_keeps_only_real_wrong_options() -> None:
    raw = {"A": "off_by_one", "B": "correct_drop", "Z": "ghost", "C": "  "}
    options = {"A": "x", "B": "y", "C": "z"}
    # B is correct → dropped; Z not an option → dropped; C blank → dropped.
    assert valid_misconceptions(raw, options, "B") == {"A": "off_by_one"}


def test_valid_misconceptions_handles_none() -> None:
    assert valid_misconceptions(None, {"A": "x", "B": "y"}, "A") == {}


def _item(**overrides: object) -> DeriveMisconceptionsItem:
    base: dict[str, object] = {
        "stem": "Solve 2x = 6",
        "options": {"A": "x = 2", "B": "x = 3"},
        "correct_option": "B",
        "lesson_objective_id": "lop01",
    }
    base.update(overrides)
    return DeriveMisconceptionsItem(**base)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_derive_returns_index_aligned_suggestions(db, monkeypatch) -> None:
    async def fake_derive(self, *, stem, options, correct_option, objective_text=""):
        return {"A": "divides_instead_of_multiplies"}

    monkeypatch.setattr(MisconceptionDeriver, "derive", fake_derive)
    response = await ClassworkApplicationService().derive_misconceptions(
        db=db, plan_version_id="LPV-NONE", items=[_item(), _item()]
    )
    assert len(response.items) == 2
    assert response.items[0].option_misconceptions == {"A": "divides_instead_of_multiplies"}


@pytest.mark.asyncio
async def test_derive_failure_yields_empty_map_not_error(db, monkeypatch) -> None:
    async def boom(self, **kwargs):
        raise RuntimeError("llm unavailable")

    monkeypatch.setattr(MisconceptionDeriver, "derive", boom)
    response = await ClassworkApplicationService().derive_misconceptions(
        db=db, plan_version_id="LPV-NONE", items=[_item()]
    )
    assert response.items[0].option_misconceptions == {}
