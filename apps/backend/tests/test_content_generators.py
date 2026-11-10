"""The generators registered for each content type, and which one a request resolves to."""

from __future__ import annotations

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import CURRENT_PIPELINE
from app.domains.content.application.errors import ContentError
from app.domains.content.domain.generators import GeneratorKind, GeneratorStatus, SchemaSource
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.models import ContentTypeGeneratorRecord
from app.domains.content.seed import seed_generators
from migrations.data.content_registry_seed import seed_content_generators, seed_content_registry


async def _seeded(db: AsyncSession) -> None:
    await (await db.connection()).run_sync(seed_content_registry)


@pytest.mark.asyncio
async def test_seeding_twice_adds_each_generator_once(db: AsyncSession) -> None:
    await _seeded(db)
    stored = await db.scalar(select(func.count()).select_from(ContentTypeGeneratorRecord))
    assert stored == len(seed_generators())
    assert await (await db.connection()).run_sync(seed_content_generators) == 0


def test_the_revision_notes_default_is_the_pipeline_the_code_defaults_to() -> None:
    defaults = {
        b.level: b.ref
        for b in seed_generators()
        if b.type_slug == BuiltIn.REVISION_NOTE.value and b.status is GeneratorStatus.DEFAULT
    }
    assert defaults == {Level.CLASS: CURRENT_PIPELINE.value, Level.LEARNER: CURRENT_PIPELINE.value}


@pytest.mark.asyncio
async def test_a_request_resolves_to_the_default_unless_it_pins_an_available_generator(
    db: AsyncSession,
) -> None:
    await _seeded(db)
    catalogue = build_content_catalogue()
    note = await catalogue.type(db, BuiltIn.REVISION_NOTE.value)

    assert (await catalogue.generator(db, note, Level.CLASS)).ref == CURRENT_PIPELINE.value
    pinned = await catalogue.generator(db, note, Level.CLASS, "2026-08-25")
    assert (pinned.harness, pinned.schema, pinned.ref) == (
        GeneratorKind.DSPY_PIPELINE,
        SchemaSource.CODE,
        "2026-08-25",
    )
    with pytest.raises(ContentError) as unknown:
        await catalogue.generator(db, note, Level.CLASS, "2020-01-01")
    assert unknown.value.detail == "unknown_generator:revision-note:2020-01-01"


@pytest.mark.asyncio
async def test_an_engine_type_without_a_row_resolves_to_the_engine_at_its_current_spec(
    db: AsyncSession,
) -> None:
    await _seeded(db)
    catalogue = build_content_catalogue()
    exam = await catalogue.type(db, "exam-questions")

    binding = await catalogue.generator(db, exam, Level.CLASS)

    assert (binding.harness, binding.schema, binding.ref) == (
        GeneratorKind.ENGINE,
        SchemaSource.SPEC,
        "exam-questions",
    )
    assert binding.spec_revision == (await catalogue.current(db, "exam-questions")).revision
    assert binding.provenance() == {
        "harness": "engine",
        "schema": "spec",
        "ref": "exam-questions",
        "spec_revision": binding.spec_revision,
    }


@pytest.mark.asyncio
async def test_a_type_and_level_hold_one_default(db: AsyncSession) -> None:
    await _seeded(db)
    second = ContentTypeGeneratorRecord(
        type_slug=BuiltIn.REVISION_NOTE.value,
        level=Level.CLASS.value,
        harness=GeneratorKind.ENGINE.value,
        schema_source=SchemaSource.SPEC.value,
        ref="plugin",
        status=GeneratorStatus.DEFAULT.value,
        default_key=f"{BuiltIn.REVISION_NOTE.value}:{Level.CLASS.value}",
    )
    db.add(second)
    with pytest.raises(IntegrityError):
        await db.flush()
