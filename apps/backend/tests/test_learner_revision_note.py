"""A learner's revision note written by the engine: adapted to their work, held to its limits."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.wiring import build_artefact_service
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.assessments.application.service import AssessmentApplicationService
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.generators import GeneratorKind
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.infrastructure.wiring import build_content_service
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.infrastructure.engine import EngineIncompleteError, Request
from app.domains.learners.models import LearnerProfile
from tests.content_engine_support import PLAN, ScriptedWriter, engine_over
from tests.plugin_folder import read_plugin
from tests.test_revision_note_generator import _installed, _section

LEARNER_WRITER = Path(__file__).parents[3] / "plugins" / "revision-note"
NOTE = BuiltIn.REVISION_NOTE.value
STUDENT = "ST-LN-1"


async def _class_note_approved(db: AsyncSession) -> Artefact:
    await _installed(db)
    built = await engine_over(db, ScriptedWriter({"lop01": [_section()]})).build(
        Request(type=NOTE, plan_version_id=PLAN)
    )
    pack = await db.scalar(select(Artefact).where(Artefact.artefact_id == built.saved_as))
    assert pack is not None
    return await build_artefact_service().approve_artefact(db=db, artefact=pack, reviewed_by="T")


async def _learner(db: AsyncSession, *, marked: int = 2, misconception: str | None = None) -> None:
    db.add(LearnerProfile(student_id=STUDENT, full_name="Ada", grade="JSS1", track="General"))
    objective = {"lesson_objective_id": "lop01", "score": 1, "max_score": marked, "items": []}
    if misconception:
        objective["misconception_code"] = misconception
    await AssessmentApplicationService().persist_diagnostic(
        db=db,
        student_id=STUDENT,
        plan_version_id=PLAN,
        results={"objectives": [objective]},
        diagnostic_id="DG-LN-1",
        survey_pending=False,
    )
    await db.flush()


async def _with_the_learner_writer_installed(db: AsyncSession) -> None:
    plugin, problems = read_plugin(LEARNER_WRITER, "revision-note-learner-writer")
    assert plugin is not None, problems
    await PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(LEARNER_WRITER), "Researcher"
    )


async def _with_the_learner_writer_as_default(db: AsyncSession) -> None:
    await _with_the_learner_writer_installed(db)
    catalogue = build_content_catalogue()
    await catalogue.make_default(db, NOTE, Level.LEARNER, "revision-note-learner-writer", "T")


def _part(**changes: object) -> dict[str, object]:
    part = dict(_section())
    part["misconception_repair"] = (
        "A common slip is to add the denominators too, which gives 3/8. The pieces are the same "
        "size, so only the numerators are added."
    )
    return {**part, **changes}


async def _written(db: AsyncSession, part: dict[str, object]) -> Artefact:
    built = await engine_over(db, ScriptedWriter({"lop01": [part]})).build(
        Request(type=NOTE, plan_version_id=PLAN, student_id=STUDENT)
    )
    stored = await db.scalar(select(Artefact).where(Artefact.artefact_id == built.saved_as))
    assert stored is not None
    return stored


@pytest.mark.asyncio
async def test_the_shipped_learner_plugin_is_a_learner_level_generator(db: AsyncSession) -> None:
    await _installed(db)
    await _with_the_learner_writer_as_default(db)
    catalogue = build_content_catalogue()

    binding = await catalogue.generator(db, await catalogue.type(db, NOTE), Level.LEARNER)

    assert (binding.ref, binding.harness, binding.level) == (
        "revision-note-learner-writer",
        GeneratorKind.ENGINE,
        Level.LEARNER,
    )
    assert (await catalogue.generator(db, await catalogue.type(db, NOTE), Level.CLASS)).ref != (
        "revision-note-learner-writer"
    )


@pytest.mark.asyncio
async def test_a_learners_note_is_stored_pending_from_the_class_version_with_its_repair(
    db: AsyncSession,
) -> None:
    class_pack = await _class_note_approved(db)
    await _learner(db, misconception="ADD_DENOMINATORS")
    await _with_the_learner_writer_as_default(db)

    stored = await _written(db, _part())

    assert (stored.scope, stored.student_id, stored.review_status.value) == (
        "learner_level",
        STUDENT,
        "pending",
    )
    assert stored.artefact_refs["made_from"] == {
        "artefact_id": class_pack.artefact_id,
        "version": class_pack.version,
    }
    assert stored.artefact_refs["generator"]["ref"] == "revision-note-learner-writer"
    assert {o["outcome"] for o in stored.artefact_refs["personalisation"]} == {"personalised"}
    assert all(
        set(o["parameters"])
        == {"explanation", "worked_support", "practice_start", "hints", "misconception_repair"}
        and o["parameters"]["misconception_repair"] is True
        for o in stored.artefact_refs["personalisation"]
    )
    sections = review_pack_manifest_to_sections(PostClassReviewPack.model_validate(stored.manifest))
    kinds = [block.block_type for block in sections[0].blocks]
    assert "misconception_repair" in kinds
    held = {c["check"] for c in stored.artefact_refs["review"]["checks"]}
    assert {"adaptation_limits", "misconception_repair", "explanation_present"} <= held


@pytest.mark.asyncio
async def test_the_learner_note_keeps_the_class_note_title_whatever_the_writer_titles_it(
    db: AsyncSession,
) -> None:
    await _class_note_approved(db)
    await _learner(db, misconception="ADD_DENOMINATORS")
    await _with_the_learner_writer_as_default(db)

    stored = await _written(db, _part(title="A different title"))

    titles = [
        s.title
        for s in review_pack_manifest_to_sections(
            PostClassReviewPack.model_validate(stored.manifest)
        )
    ]
    assert "A different title" not in titles
    assert _section()["title"] in titles


@pytest.mark.asyncio
async def test_a_misconception_is_repaired_where_the_state_names_one_and_nowhere_else(
    db: AsyncSession,
) -> None:
    await _class_note_approved(db)
    await _learner(db, misconception="ADD_DENOMINATORS")
    await _with_the_learner_writer_as_default(db)
    bare = _part()
    del bare["misconception_repair"]

    with pytest.raises(EngineIncompleteError) as missing:
        await _written(db, bare)

    assert "write misconception_repair" in str(missing.value)


@pytest.mark.asyncio
async def test_a_repair_for_a_misconception_the_state_does_not_name_is_left_out_of_the_note(
    db: AsyncSession,
) -> None:
    await _class_note_approved(db)
    await _learner(db)
    await _with_the_learner_writer_as_default(db)

    stored = await _written(db, _part())

    sections = review_pack_manifest_to_sections(PostClassReviewPack.model_validate(stored.manifest))
    assert "misconception_repair" not in [b.block_type for b in sections[0].blocks]
    assert all("parameters" in o for o in stored.artefact_refs["personalisation"])


@pytest.mark.asyncio
async def test_a_learner_with_too_little_marked_work_gets_the_class_note_as_it_stands(
    db: AsyncSession,
) -> None:
    from app.domains.content.infrastructure.wiring import build_engine_learner_generator

    class_pack = await _class_note_approved(db)
    await _learner(db, marked=1)
    await _with_the_learner_writer_as_default(db)
    catalogue = build_content_catalogue()
    binding = await catalogue.generator(db, await catalogue.type(db, NOTE), Level.LEARNER)

    made = await build_engine_learner_generator().generate(
        db, plan_version_id=PLAN, student_id=STUDENT, binding=binding
    )

    stored = await db.scalar(select(Artefact).where(Artefact.artefact_id == made))
    assert stored is not None
    kept = [[b.get("content") for b in step["blocks"]] for step in stored.manifest["steps"]]
    assert kept == [[b.get("content") for b in s["blocks"]] for s in class_pack.manifest["steps"]]
    assert {o["outcome"] for o in stored.artefact_refs["personalisation"]} == {"thin_evidence"}
    assert all("parameters" not in o for o in stored.artefact_refs["personalisation"])


@pytest.mark.asyncio
async def test_the_job_uses_the_engine_only_when_the_learner_default_is_an_engine_generator(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.domains.assessments.jobs import _written_by_the_engine
    from app.domains.content.infrastructure import wiring

    class _Generator:
        async def generate(self, db, *, plan_version_id, student_id, binding):  # type: ignore[no-untyped-def]
            return f"AT-by-{binding.ref}"

    monkeypatch.setattr(wiring, "build_engine_learner_generator", _Generator)
    await _installed(db)
    assert await _written_by_the_engine(db, STUDENT, PLAN) is None

    await _with_the_learner_writer_as_default(db)

    assert await _written_by_the_engine(db, STUDENT, PLAN) == "AT-by-revision-note-learner-writer"


@pytest.mark.asyncio
async def test_a_pinned_generator_that_is_not_the_default_writes_to_its_own_spec(
    db: AsyncSession,
) -> None:
    await _class_note_approved(db)
    await _learner(db, misconception="ADD_DENOMINATORS")
    await _with_the_learner_writer_installed(db)
    catalogue = build_content_catalogue()
    default = await catalogue.generator(db, await catalogue.type(db, NOTE), Level.LEARNER)
    assert default.ref != "revision-note-learner-writer"

    built = await engine_over(db, ScriptedWriter({"lop01": [_part()]})).build(
        Request(
            type=NOTE,
            plan_version_id=PLAN,
            student_id=STUDENT,
            generator="revision-note-learner-writer",
        )
    )

    stored = await db.scalar(select(Artefact).where(Artefact.artefact_id == built.saved_as))
    assert stored is not None
    assert stored.artefact_refs["generator"]["ref"] == "revision-note-learner-writer"


@pytest.mark.asyncio
async def test_a_second_class_revision_note_from_the_engine_is_refused_before_the_model_runs(
    db: AsyncSession,
) -> None:
    await _class_note_approved(db)

    with pytest.raises(ContentError) as refused:
        await build_content_service().check_generation(
            db,
            plan_version_id=PLAN,
            type=NOTE,
            level=Level.CLASS,
            choices=GenerationChoices(),
        )

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "lesson_already_has_a_class_revision_note",
    )


@pytest.mark.asyncio
async def test_a_check_is_listed_once_though_the_validator_and_the_store_both_held_the_note_to_it(
    db: AsyncSession,
) -> None:
    await _class_note_approved(db)
    await _learner(db, misconception="ADD_DENOMINATORS")
    await _with_the_learner_writer_as_default(db)

    stored = await _written(db, _part())

    names = [c["check"] for c in stored.artefact_refs["review"]["checks"]]
    assert len(names) == len(set(names))
