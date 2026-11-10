"""A plugin that implements the revision note writes the sections the class pack is made of."""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content.infrastructure.wiring import build_content_service
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.infrastructure.engine import (
    EngineIncompleteError,
    EngineRefusedError,
    Request,
)
from app.domains.teaching.models.syllabus import LessonPeriod
from tests.content_engine_support import (
    PLAN,
    SESSION_PLAN,
    ScriptedWriter,
    engine_over,
    seed_lesson,
)
from tests.plugin_folder import read_plugin

WRITER = Path(__file__).parents[3] / "plugins" / "revision-note"
NOTE = BuiltIn.REVISION_NOTE.value


_EXPLANATION = (
    "Fractions with the same denominator are parts of a whole cut into the same number of equal "
    "pieces, so you can add them by counting pieces. The denominator names the size of a piece "
    "and stays as it is; the numerator counts the pieces, so the numerators are added. For "
    "example, one quarter and two quarters make three quarters, which is $\\frac{3}{4}$. A "
    "common slip is to add the denominators as well and write $\\frac{3}{8}$, but the pieces "
    "have not become smaller, so the denominator must not change."
)


def _example(first: int, second: int) -> dict[str, object]:
    total = first + second
    return {
        "problem": f"Find $\\frac{{{first}}}{{9}}+\\frac{{{second}}}{{9}}$.",
        "solution": [
            {"working": f"$\\frac{{{first}+{second}}}{{9}}$", "commentary": "Add the numerators."},
            {"working": f"$\\frac{{{total}}}{{9}}$", "commentary": "Keep the denominator."},
        ],
        "answer": f"$\\frac{{{total}}}{{9}}$",
    }


def _question(first: int, second: int) -> dict[str, object]:
    return {
        "question": f"Find $\\frac{{{first}}}{{8}}+\\frac{{{second}}}{{8}}$.",
        "answer": f"$\\frac{{{first + second}}}{{8}}$",
        "worked_solution": f"Add the numerators, {first}+{second}, and keep the 8.",
    }


def _section(title: str = "Adding fractions") -> dict[str, object]:
    return {
        "title": title,
        "explanation": _EXPLANATION,
        "figures": [
            {
                "caption": "A bar split in four",
                "drawing": "\\begin{tikzpicture}\\draw (0,0) rectangle (4,1);\\end{tikzpicture}",
            }
        ],
        "worked_examples": [_example(1, 2), _example(3, 4)],
        "practice": [_question(1, 2), _question(2, 3), _question(1, 5)],
    }


async def _installed(db: AsyncSession) -> None:
    await seed_lesson(db)
    await db.execute(
        update(PlanVersion)
        .where(PlanVersion.version_id == PLAN)
        .values(session_plan={**SESSION_PLAN, "references": ["Mathematics Made Easy, page 12"]})
    )
    period = uuid.uuid4()
    db.add_all(
        [
            LessonPeriod(
                id=period, scheme_of_work_id=uuid.uuid4(), period_number=1, subtopic_id="sub-1"
            ),
            LessonPlan(
                plan_id="P-ENGINE-1",
                lesson_period_id=period,
                title="Adding fractions",
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
        ]
    )
    await db.flush()
    plugin, problems = read_plugin(WRITER, "revision-note-writer")
    assert plugin is not None, problems
    catalogue = build_content_catalogue()
    await PluginInstaller(catalogue, SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(WRITER), "Researcher"
    )
    await catalogue.make_default(db, NOTE, Level.CLASS, "revision-note-writer", "Researcher")


@pytest.mark.asyncio
async def test_the_sections_are_stored_as_the_class_pack_the_pipeline_would_store(
    db: AsyncSession,
) -> None:
    await _installed(db)
    writer = ScriptedWriter({"lop01": [_section()]})

    built = await engine_over(db, writer).build(Request(type=NOTE, plan_version_id=PLAN))

    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert (record.type, record.kind, record.level) == (NOTE, "post_class_review_pack", Level.CLASS)
    assert record.review_status == "pending"
    assert record.review is not None and record.review["version"] == 1
    assert {c["check"]: c["passed"] for c in record.review["checks"]}["explanation_present"]
    assert record.provenance["generator"] == {
        "harness": "engine",
        "schema": "spec",
        "ref": "revision-note-writer",
        "spec_revision": 2,
    }
    sections = review_pack_manifest_to_sections(PostClassReviewPack.model_validate(record.manifest))
    # The pack is stored by lesson step, as the pipeline stores it: each step of the
    # objective carries the objective's section.
    assert {section.title for section in sections} == {"Adding fractions"}
    section = sections[0]
    assert "tikzpicture" in section.blocks[0].text
    assert section.blocks[0].source_refs
    assert section.practice[0].answer.startswith("$\\frac{3}{8}$")
    assert "keep the 8" in section.practice[0].answer


@pytest.mark.asyncio
async def test_a_lesson_with_a_class_pack_takes_no_second_one(db: AsyncSession) -> None:
    await _installed(db)
    await engine_over(db, ScriptedWriter({"lop01": [_section()]})).build(
        Request(type=NOTE, plan_version_id=PLAN)
    )

    with pytest.raises(EngineRefusedError, match="already has a class revision note"):
        await engine_over(db, ScriptedWriter({"lop01": [_section("Again")]})).build(
            Request(type=NOTE, plan_version_id=PLAN)
        )


@pytest.mark.asyncio
async def test_a_thin_section_goes_back_to_the_writer_with_what_it_lacks(
    db: AsyncSession,
) -> None:
    await _installed(db)
    thin = {**_section(), "explanation": "Add the numerators.", "worked_examples": [_example(1, 2)]}
    thin["practice"] = [_question(1, 2), _question(1, 2)]
    writer = ScriptedWriter({"lop01": [thin]})

    with pytest.raises(EngineIncompleteError) as sent_back:
        await engine_over(db, writer).build(Request(type=NOTE, plan_version_id=PLAN))

    message = str(sent_back.value)
    for lack in (
        "the explanation holds 19 characters",
        "at least 2 worked examples",
        "at least 3 practice questions",
        "two practice questions are the same",
    ):
        assert lack in message


@pytest.mark.asyncio
async def test_a_practice_question_that_is_a_worked_example_and_a_false_size_rule_go_back(
    db: AsyncSession,
) -> None:
    await _installed(db)
    section = _section()
    section["practice"] = [
        {"question": section["worked_examples"][0]["problem"], "answer": "3"},  # type: ignore[index]
        _question(2, 3),
        _question(1, 5),
    ]
    section["explanation"] = f"{_EXPLANATION} The larger unit name always wins."
    writer = ScriptedWriter({"lop01": [section]})

    with pytest.raises(EngineIncompleteError) as sent_back:
        await engine_over(db, writer).build(Request(type=NOTE, plan_version_id=PLAN))

    assert "is a worked example again" in str(sent_back.value)
    assert "larger unit name or leading digit" in str(sent_back.value)


@pytest.mark.asyncio
async def test_a_lesson_whose_class_note_was_rejected_takes_a_new_one(db: AsyncSession) -> None:
    await _installed(db)
    first = await engine_over(db, ScriptedWriter({"lop01": [_section()]})).build(
        Request(type=NOTE, plan_version_id=PLAN)
    )
    await db.execute(
        update(Artefact)
        .where(Artefact.artefact_id == first.saved_as)
        .values(review_status=ArtefactReviewStatus.REJECTED)
    )
    await db.commit()

    second = await engine_over(db, ScriptedWriter({"lop01": [_section("Again")]})).build(
        Request(type=NOTE, plan_version_id=PLAN)
    )

    assert second.saved_as != first.saved_as


@pytest.mark.asyncio
async def test_the_app_can_ask_for_a_revision_note_grounded_in_the_lesson_note_from_the_engine(
    db: AsyncSession,
) -> None:
    await _installed(db)
    service = build_content_service()

    async def ask(sources: str | None) -> None:
        await service.check_generation(
            db,
            plan_version_id=PLAN,
            type=NOTE,
            level=Level.CLASS,
            choices=GenerationChoices(sources=sources),
        )

    await ask(None)
    await ask("lesson-note")
    with pytest.raises(ContentError) as refused:
        await ask("textbook")
    assert refused.value.detail == "sources_apply_to_the_pipeline_only"
