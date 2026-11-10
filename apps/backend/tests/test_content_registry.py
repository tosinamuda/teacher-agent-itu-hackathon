"""Specifications are data: a seed file, then versioned rows the app reads and injects."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path

import pytest

from app.domains.artefacts.core.domain.registry import ContentRegistry
from app.domains.artefacts.core.domain.specification import (
    ContentSpecification,
    specification_ref,
)
from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.specifications.seed import seed_specification, seed_specifications
from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)

STUDY_FINGERPRINT = Path("experiments/h1_condition_eval/runs/c0c3-prism-objective/fingerprint.json")
CLASS = frozenset({ArtefactScope.CLASS_LEVEL})
BOTH = frozenset({ArtefactScope.CLASS_LEVEL, ArtefactScope.LEARNER_LEVEL})


def _spec(**overrides: object) -> ContentSpecification:
    fields: dict[str, object] = {
        "kind": ArtefactType.LESSON_NOTE.value,
        "revision": 1,
        "material": "a lesson note",
        "audience": "{reader}",
        "levels": CLASS,
        "structure": ("steps",),
        "requirements": ("stay on the objective",),
    }
    fields.update(overrides)
    return ContentSpecification(**fields)  # type: ignore[arg-type]


def test_the_seed_holds_every_kind_at_its_current_revision() -> None:
    seeded = seed_specifications()

    assert seeded.kinds() == (
        ArtefactType.POST_CLASS_REVIEW_PACK.value,
        ArtefactType.DIAGNOSTIC.value,
        ArtefactType.LESSON_NOTE.value,
        ArtefactType.LESSON_PLAN.value,
        "exam_questions",
    )
    assert {kind: seeded.specification(kind).revision for kind in seeded.kinds()} == {
        ArtefactType.POST_CLASS_REVIEW_PACK: 1,
        ArtefactType.DIAGNOSTIC: 1,
        ArtefactType.LESSON_NOTE: 1,
        ArtefactType.LESSON_PLAN: 7,
        "exam_questions": 2,
    }


def test_the_plan_spec_asks_its_generator_what_the_study_s_plans_were_asked() -> None:
    """Revisions 3 and 4 change only the parts a plan is drafted in; the brief is revision 2's."""
    record = seed_specifications().specification(ArtefactType.LESSON_PLAN.value).to_record()
    brief = {
        name: record[name]
        for name in ("material", "audience", "levels", "structure", "requirements", "adaptable")
    }
    digest = hashlib.sha256(json.dumps(brief, sort_keys=True).encode()).hexdigest()[:12]

    assert digest == "eb8c3cec2264"


def test_the_seeded_pack_brief_is_the_one_the_evaluated_study_sent() -> None:
    """The study fingerprinted its brief; the seed must reproduce that digest exactly."""
    recorded = json.loads(STUDY_FINGERPRINT.read_text())["inputs"]["artefact_spec"]
    seeded = revision_pack_spec("JSS1").model_dump_json()

    assert hashlib.sha256(seeded.encode()).hexdigest()[:12] == recorded


def test_the_brief_is_read_from_the_specification_it_is_given() -> None:
    edited = ContentSpecification.from_record(
        {
            **seed_specification(ArtefactType.POST_CLASS_REVIEW_PACK.value).to_record(),
            "revision": 2,
            "requirements": ["Only this."],
        }
    )

    assert revision_pack_spec("JSS1", edited).requirements == ["Only this."]
    with pytest.raises(ValueError, match="not_a_revision_pack_specification"):
        revision_pack_spec("JSS1", seed_specification(ArtefactType.DIAGNOSTIC.value))


def test_a_record_round_trips_and_the_ref_names_kind_and_revision() -> None:
    pack = seed_specification(ArtefactType.POST_CLASS_REVIEW_PACK.value)

    assert ContentSpecification.from_record(pack.to_record()) == pack
    assert specification_ref(pack) == {
        "specification": {"kind": "post_class_review_pack", "revision": 1}
    }


def test_learner_level_content_declares_what_adaptation_may_change() -> None:
    with pytest.raises(ValueError, match="must declare what adaptation may change"):
        _spec(levels=BOTH)


def test_class_level_content_declares_nothing_adaptable() -> None:
    with pytest.raises(ValueError, match="only learner-level content is adapted"):
        _spec(adaptable=("difficulty",))


def test_a_kind_registers_once_and_an_unknown_kind_is_refused() -> None:
    registry = ContentRegistry([_spec()])

    with pytest.raises(ValueError, match="content_already_registered:lesson_note"):
        registry.register(_spec())
    with pytest.raises(ValueError, match="unknown_content:post_class_review_pack"):
        registry.specification(ArtefactType.POST_CLASS_REVIEW_PACK.value)


def test_the_listing_route_is_mounted() -> None:
    from fastapi.routing import APIRoute

    from app.main import app

    assert "/content/types" in {r.path for r in app.routes if isinstance(r, APIRoute)}


def test_the_app_wires_the_database_store_into_pack_generation(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    from app.domains.artefacts.core.infrastructure.specifications import (
        SqlAlchemyContentSpecifications,
    )
    from app.domains.artefacts.types.post_class_review_pack.infrastructure import wiring
    from tests.condition_leakage_support import EchoModel, stand_in_collaborators

    monkeypatch.setattr(
        wiring, "live_section_collaborators", lambda *_: stand_in_collaborators(EchoModel())
    )

    assert isinstance(
        wiring.build_student_pack_service().specifications, SqlAlchemyContentSpecifications
    )


def test_the_app_wires_the_database_store_into_class_test_generation() -> None:
    from app.domains.artefacts.core.infrastructure.specifications import (
        SqlAlchemyContentSpecifications,
    )
    from app.domains.assessments.infrastructure.wiring import build_diagnostic_service

    assert isinstance(build_diagnostic_service().specifications, SqlAlchemyContentSpecifications)


async def _seed(db):  # type: ignore[no-untyped-def]
    from migrations.data.content_registry_seed import seed_content_specifications

    connection = await db.connection()
    return await connection.run_sync(seed_content_specifications)


@pytest.mark.asyncio
async def test_seeding_is_idempotent_and_the_store_serves_the_seed(db) -> None:
    from app.domains.artefacts.core.infrastructure.specifications import (
        SqlAlchemyContentSpecifications,
    )

    assert await _seed(db) == 5
    assert await _seed(db) == 0
    store = SqlAlchemyContentSpecifications()

    for kind in seed_specifications().kinds():
        assert await store.current(db, kind) == seed_specification(kind)
    assert [s.kind for s in await store.all_current(db)] == sorted(seed_specifications().kinds())


@pytest.mark.asyncio
async def test_a_seed_revision_whose_number_a_plugin_holds_is_stored_as_the_next_one(db) -> None:
    from sqlalchemy import select

    from app.domains.artefacts.core.infrastructure.models import ContentSpecificationRecord
    from app.domains.artefacts.core.infrastructure.specifications import (
        SqlAlchemyContentSpecifications,
    )

    kind = ArtefactType.DIAGNOSTIC.value
    seed = seed_specification(kind)
    db.add(
        ContentSpecificationRecord(
            **{**seed.to_record(), "revision": seed.revision, "generator": "a-plugin"}
        )
    )
    await db.flush()

    assert await _seed(db) == 5
    assert await _seed(db) == 0
    revisions = (
        await db.execute(
            select(ContentSpecificationRecord.revision, ContentSpecificationRecord.generator)
            .where(ContentSpecificationRecord.kind == kind)
            .order_by(ContentSpecificationRecord.revision)
        )
    ).all()
    assert [(r.revision, r.generator) for r in revisions] == [
        (seed.revision, "a-plugin"),
        (seed.revision + 1, None),
    ]
    current = await SqlAlchemyContentSpecifications().current(db, kind)
    assert current.revision == seed.revision + 1


@pytest.mark.asyncio
async def test_a_later_revision_becomes_current_and_the_first_stays_readable(db) -> None:
    from app.domains.artefacts.core.infrastructure.models import ContentSpecificationRecord
    from app.domains.artefacts.core.infrastructure.specifications import (
        SqlAlchemyContentSpecifications,
    )

    await _seed(db)
    first = seed_specification(ArtefactType.DIAGNOSTIC.value)
    db.add(
        ContentSpecificationRecord(
            **{**first.to_record(), "revision": 2, "requirements": ["Three items per objective."]}
        )
    )
    await db.flush()
    store = SqlAlchemyContentSpecifications()

    assert (await store.current(db, ArtefactType.DIAGNOSTIC.value)).revision == 2
    assert await store.revision(db, ArtefactType.DIAGNOSTIC.value, 1) == first


@pytest.mark.asyncio
async def test_the_served_prompt_from_the_stored_specification_is_the_committed_one(db) -> None:
    """Injecting the stored pack specification sends, byte for byte, the pinned prompt."""
    from app.domains.artefacts.core.infrastructure.specifications import (
        SqlAlchemyContentSpecifications,
    )
    from app.domains.experiments.domain.types import ConditionCode
    from scripts.prompt_snapshots import SERVED_DIR
    from scripts.prompt_snapshots.render import served_snapshot_text, snapshot_name
    from scripts.prompt_snapshots.served import served_arm

    await _seed(db)
    stored = await SqlAlchemyContentSpecifications().current(
        db, ArtefactType.POST_CLASS_REVIEW_PACK
    )

    for condition in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        arm = await asyncio.to_thread(served_arm, condition, stored)
        assert served_snapshot_text(arm) == (SERVED_DIR / snapshot_name(arm)).read_text()


def test_every_seeded_type_fits_its_seeded_spec() -> None:
    from app.domains.content.seed import seed_types

    specifications = seed_specifications()
    for definition in seed_types():
        definition.check(specifications.specification(definition.kind))
    assert {t.kind for t in seed_types()} == set(specifications.kinds())
