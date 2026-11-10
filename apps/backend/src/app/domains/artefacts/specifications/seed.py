"""Read the seed specifications shipped beside this module."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

from app.domains.artefacts.core.domain.registry import ContentRegistry
from app.domains.artefacts.core.domain.specification import ContentSpecification

SEED_PATH = Path(__file__).with_name("seed.json")


@cache
def seed_specifications() -> ContentRegistry:
    """The seeded revision of every kind, in the order the seed file lists them."""
    records = json.loads(SEED_PATH.read_text(encoding="utf-8"))["specifications"]
    return ContentRegistry(ContentSpecification.from_record(record) for record in records)


def seed_specification(kind: str) -> ContentSpecification:
    """The seeded revision of one kind."""
    return seed_specifications().specification(kind)
