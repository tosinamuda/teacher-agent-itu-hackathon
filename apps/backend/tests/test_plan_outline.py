"""What of a lesson plan is written so far: its objectives, and its steps in plan order."""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.parts import Unit
from app.domains.content_engine.application.plan_outline import outline_of
from app.domains.content_engine.domain.lesson import LessonUnit
from app.domains.content_engine.infrastructure.models import ContentDraftRecord
from app.domains.content_engine.infrastructure.plan_progress import drafting_outline

UNITS = (
    LessonUnit("lesson", "Word problems", Unit.LESSON),
    LessonUnit("po1", "Translate", Unit.CURRICULUM_OBJECTIVE),
    LessonUnit("po2", "Solve", Unit.CURRICULUM_OBJECTIVE),
)

LESSON_PART = {
    "intro": {"title": "Recall", "estimated_minutes": 5},
    "evaluation": {"title": "Check", "estimated_minutes": 10},
}


def objective_part(objective: str, title: str, minutes: int | None) -> dict:
    return {
        "lesson_objectives": [
            {"objective": objective, "core_step": {"title": title, "estimated_minutes": minutes}}
        ]
    }


def test_nothing_is_shown_before_anything_is_written() -> None:
    outline = outline_of(UNITS, {})

    assert outline.objectives == []
    assert outline.steps == []
    assert (outline.written, outline.total) == (0, 3)


def test_steps_come_in_plan_order_whatever_order_they_were_written_in() -> None:
    parts = {
        "po2": objective_part("Solve it.", "Solve", 20),
        "lesson": LESSON_PART,
        "po1": objective_part("Translate it.", "Translate", 15),
    }

    outline = outline_of(UNITS, parts)

    assert [step.title for step in outline.steps] == ["Recall", "Translate", "Solve", "Check"]
    assert [step.minutes for step in outline.steps] == [5, 15, 20, 10]
    assert outline.objectives == ["Translate it.", "Solve it."]
    assert (outline.written, outline.total) == (3, 3)


def test_a_part_without_a_title_or_minutes_is_left_out_or_blank() -> None:
    parts = {
        "po1": objective_part("Translate it.", "Translate", None),
        "po2": {"lesson_objectives": []},
    }

    outline = outline_of(UNITS, parts)

    assert [(step.title, step.minutes) for step in outline.steps] == [("Translate", None)]


def _draft(draft_id: str, session_id: str, status: str, parts: dict) -> ContentDraftRecord:
    return ContentDraftRecord(
        draft_id=draft_id,
        type="lesson-plan",
        kind="lesson_plan",
        spec_revision=1,
        session_id=session_id,
        unit="lesson",
        units=[{"unit_id": u.unit_id, "label": u.label, "unit": u.unit.value} for u in UNITS],
        parts=parts,
        status=status,
        created_by="engine",
    )


@pytest.mark.asyncio
async def test_the_outline_is_read_from_the_lessons_open_draft(db: AsyncSession) -> None:
    db.add_all(
        [
            _draft("DR-done", "S-1", "submitted", {"lesson": LESSON_PART}),
            _draft(
                "DR-open", "S-1", "open", {"po1": objective_part("Translate it.", "Translate", 15)}
            ),
            _draft("DR-elsewhere", "S-2", "open", {"lesson": LESSON_PART}),
        ]
    )
    await db.flush()

    outline = await drafting_outline(db, "S-1")

    assert outline is not None
    assert [step.title for step in outline.steps] == ["Translate"]
    assert (outline.written, outline.total) == (1, 3)


@pytest.mark.asyncio
async def test_a_lesson_with_no_open_draft_has_no_outline(db: AsyncSession) -> None:
    db.add(_draft("DR-done", "S-3", "submitted", {"lesson": LESSON_PART}))
    await db.flush()

    assert await drafting_outline(db, "S-3") is None
