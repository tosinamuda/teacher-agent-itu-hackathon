"""Read the built-in content types shipped beside this module."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

from app.domains.content.domain.generators import (
    GeneratorBinding,
    GeneratorKind,
    GeneratorStatus,
    SchemaSource,
)
from app.domains.content.domain.types import Audience, ContentTypeDefinition, Engine, Level

SEED_PATH = Path(__file__).with_name("seed.json")


@cache
def seed_types() -> tuple[ContentTypeDefinition, ...]:
    """The built-in types, positioned in the order the seed file lists them."""
    records = json.loads(SEED_PATH.read_text(encoding="utf-8"))["types"]
    return tuple(
        ContentTypeDefinition(
            slug=record["slug"],
            kind=record["kind"],
            label=record["label"],
            audience=Audience(record["audience"]),
            engine=Engine(record["engine"]),
            made_from_a_plan_version=bool(record["made_from_a_plan_version"]),
            position=position,
        )
        for position, record in enumerate(records, start=1)
    )


@cache
def seed_generators() -> tuple[GeneratorBinding, ...]:
    """The generators each built-in type has today, with the one that is the default."""
    records = json.loads(SEED_PATH.read_text(encoding="utf-8"))["generators"]
    return tuple(
        GeneratorBinding(
            type_slug=record["type"],
            level=Level(record["level"]),
            harness=GeneratorKind(record["harness"]),
            schema=SchemaSource(record["schema"]),
            ref=record["ref"],
            status=GeneratorStatus(record["status"]),
        )
        for record in records
    )
