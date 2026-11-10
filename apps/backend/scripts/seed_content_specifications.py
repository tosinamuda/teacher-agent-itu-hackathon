"""Seed the built-in content types, skills, every kind's seed specification and generators.

Invocation::

    uv run python -m scripts.seed_content_specifications

Idempotent: adds only the types, (skill, revision) and (kind, revision) rows not already
stored. The deploy
runs it on every release, so a new built-in type or spec revision ships with its code.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.content_registry_seed import seed_content_registry


def main() -> int:
    with sync_engine.begin() as conn:
        types, skills, specifications, generators = seed_content_registry(conn)
    print(
        "content registry seed complete: "
        f"types added = {types}, skills added = {skills}, specs added = {specifications}, "
        f"generators added = {generators}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
