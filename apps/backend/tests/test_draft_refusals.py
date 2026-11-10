"""A refused write says what state the part is in, so the writer's next call is the right one."""

from __future__ import annotations

import pytest

from app.domains.artefacts.core.domain.parts import PartSchema, Unit
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.domains.content_engine.domain.lesson import LessonUnit


class _Spec:
    """Just enough of a spec: one text field every part must have."""

    def schema_for(self, _unit: Unit) -> PartSchema:
        return PartSchema.from_record(
            [{"name": "title", "description": "A heading", "type": "text"}]
        )


def _draft(parts: dict | None = None) -> Draft:
    return Draft(
        draft_id="D1",
        type="t",
        kind="k",
        spec_revision=1,
        plan_version_id=None,
        session_id="S",
        unit=Unit.LESSON,
        units=(LessonUnit("u1", "One", Unit.LESSON),),
        parts=parts or {},
    )


def test_a_refused_new_part_says_nothing_was_stored_and_to_add_it_again() -> None:
    draft = _draft()

    with pytest.raises(DraftError) as refused:
        draft.put("u1", {"title": ""}, _Spec(), replace=False)  # type: ignore[arg-type]

    assert "title: must be text that is not empty" in str(refused.value)
    assert "Nothing was stored" in str(refused.value)
    assert "add_part" in str(refused.value)
    assert draft.parts == {}


def test_a_refused_revision_says_the_part_is_unchanged() -> None:
    draft = _draft({"u1": {"title": "Kept"}})

    with pytest.raises(DraftError) as refused:
        draft.put("u1", {"title": ""}, _Spec(), replace=True)  # type: ignore[arg-type]

    assert "unchanged" in str(refused.value)
    assert draft.parts == {"u1": {"title": "Kept"}}
