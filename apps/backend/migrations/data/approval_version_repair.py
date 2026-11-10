r"""Give each approved artefact the version its approval names.

Approving an artefact used to add one to its version, though the approval changed no content,
so a page read "Version 3" while its history said "Approved version 2". Approval now leaves
the version alone. This takes the extra one off every approved artefact that still carries it:
one whose version is exactly one past the version its latest approval names. Content of a
concluded lesson is read-only and is left as it is.

Idempotent: a repaired artefact's version equals its approved version, so it no longer matches.

CLI: ``uv run python -m migrations.data.approval_version_repair [--dry-run]``.
"""

from __future__ import annotations

import argparse

import sqlalchemy as sa

from app.db.config import get_sync_database_url

_STILL_BUMPED = """
    FROM artefacts
    WHERE review_status = 'approved'
      AND version = 1 + (
          SELECT MAX(content_approvals.approved_version)
          FROM content_approvals
          WHERE content_approvals.artefact_id = artefacts.artefact_id
      )
      AND plan_version_id NOT IN (
          SELECT version_id FROM plan_versions WHERE concluded_at IS NOT NULL
      )
"""


def repair_approval_versions(connection: sa.Connection, *, dry_run: bool = False) -> int:
    """Take the approval's extra version off each approved artefact; return how many."""
    if dry_run:
        return int(connection.execute(sa.text(f"SELECT COUNT(*) {_STILL_BUMPED}")).scalar_one())
    result = connection.execute(
        sa.text(
            "UPDATE artefacts SET version = version - 1 WHERE artefact_id IN "
            f"(SELECT artefact_id FROM (SELECT artefact_id {_STILL_BUMPED}) AS bumped)"
        )
    )
    return int(result.rowcount or 0)


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="Count, write nothing.")
    args = parser.parse_args()
    engine = sa.create_engine(get_sync_database_url())
    with engine.begin() as connection:
        count = repair_approval_versions(connection, dry_run=args.dry_run)
    verb = "would repair" if args.dry_run else "repaired"
    print(f"approved artefact versions {verb}: {count}")


if __name__ == "__main__":
    _main()
