r"""Give every existing class test its material record.

A class test's questions live in ``exit_ticket_items``; generation and manual classwork now
also write a material record per plan version, which the materials API, the approval log
and the revision history address. Class tests made before that have items but no record.
This creates one for each, pending — or approved, with the release as its approval, where
the class test was already sent to students.

Idempotent: a plan version that already has a class-test record is left untouched.

CLI: ``uv run python -m migrations.data.class_test_material_backfill [--dry-run]``.
"""

from __future__ import annotations

import argparse
import uuid

import sqlalchemy as sa

from app.db.config import get_sync_database_url
from app.shared.ids import PublicIdPrefix, new_public_id

_ARTEFACTS = sa.table(
    "artefacts",
    sa.column("id", sa.Uuid),
    sa.column("artefact_id"),
    sa.column("artefact_kind"),
    sa.column("scope"),
    sa.column("plan_version_id"),
    sa.column("manifest", sa.JSON),
    sa.column("version"),
    sa.column("review_status"),
    sa.column("reviewed_at"),
    sa.column("reviewed_by"),
)
_APPROVALS = sa.table(
    "content_approvals",
    sa.column("id", sa.Uuid),
    sa.column("approval_id"),
    sa.column("artefact_id"),
    sa.column("approved_version"),
    sa.column("approved_by"),
    sa.column("approved_at"),
)
_WITHOUT_RECORD = sa.text(
    """
    SELECT items.plan_version_id, plans.assessment_released_at, plans.assessment_released_by
    FROM (SELECT DISTINCT plan_version_id FROM exit_ticket_items) AS items
    JOIN plan_versions AS plans ON plans.version_id = items.plan_version_id
    WHERE NOT EXISTS (
        SELECT 1 FROM artefacts
        WHERE artefacts.artefact_kind = 'diagnostic'
          AND artefacts.plan_version_id = items.plan_version_id
    )
    """
)


def backfill_class_test_materials(connection: sa.Connection, *, dry_run: bool = False) -> int:
    """Create the missing records. Returns how many plan versions needed one."""
    missing = connection.execute(_WITHOUT_RECORD).all()
    if dry_run:
        return len(missing)
    for plan_version_id, released_at, released_by in missing:
        artefact_id = new_public_id(PublicIdPrefix.ARTEFACT)
        released = released_at is not None
        connection.execute(
            _ARTEFACTS.insert().values(
                id=uuid.uuid4(),
                artefact_id=artefact_id,
                artefact_kind="diagnostic",
                scope="class_level",
                plan_version_id=plan_version_id,
                manifest={"plan_version_id": plan_version_id, "source": "backfill"},
                version=1,
                review_status="approved" if released else "pending",
                reviewed_at=released_at,
                reviewed_by=released_by,
            )
        )
        if released:
            connection.execute(
                _APPROVALS.insert().values(
                    id=uuid.uuid4(),
                    approval_id=new_public_id(PublicIdPrefix.CONTENT_APPROVAL),
                    artefact_id=artefact_id,
                    approved_version=1,
                    approved_by=released_by,
                    approved_at=released_at,
                )
            )
    return len(missing)


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="Count, write nothing.")
    args = parser.parse_args()
    engine = sa.create_engine(get_sync_database_url())
    with engine.begin() as connection:
        count = backfill_class_test_materials(connection, dry_run=args.dry_run)
    verb = "would create" if args.dry_run else "created"
    print(f"class-test material records {verb}: {count}")


if __name__ == "__main__":
    _main()
