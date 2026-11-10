"""File every experiment into a study (``experiments.investigation_db_id``).

The study becomes the explicit parent of the experiment. Existing experiments
carry no parent FK; this derives one:

  * An experiment whose ``lesson_period_id`` was scoped by the existing demo study
    (the oldest investigation, via the soon-to-be-dropped ``investigation_lessons``
    join table) stays in that study.
  * Every other experiment — including legacy rows with a NULL ``lesson_period_id``
    — is filed into a single global "Unfiled experiments" study (``INV-UNFILED``).

Idempotent: the Unfiled study is keyed by ``investigation_code = 'INV-UNFILED'``,
and updates are guarded by ``investigation_db_id IS NULL``. Safe to re-run after
``investigation_lessons`` is dropped (the demo-scope step is skipped if the table
is gone).

Run AFTER ``20260608_study_parent_a`` and BEFORE ``20260608_study_parent_b``.
Invocation: see ``scripts/seed_experiment_investigation.py``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import sqlalchemy as sa

from app.shared.ids import PublicIdPrefix, new_public_id

UNFILED_CODE = "INV-UNFILED"
UNFILED_TITLE = "Unfiled experiments"
UNFILED_DESCRIPTION = "Experiments not yet filed into a study."


def _uuid_hex(value: object) -> str:
    """Normalise a raw-SQL uuid value to 32-char hex.

    Raw ``sa.text`` reads bypass the ORM ``Uuid`` type, so the value comes back as
    the bare ``CHAR(32)`` hex MySQL stores. ``.hex`` is the canonical form to bind
    back into the column.
    """
    return uuid.UUID(str(value)).hex


@dataclass(frozen=True)
class _BackfillReport:
    unfiled_created: bool
    filed_into_demo: int
    filed_into_unfiled: int
    residual_null: int


def backfill_experiment_investigation(conn: sa.Connection) -> _BackfillReport:
    """Give every experiment a parent study, preserving the demo study's members."""
    # The demo study = the oldest pre-existing investigation that is not Unfiled.
    demo_id = conn.execute(
        sa.text(
            """
            SELECT id FROM investigations
            WHERE investigation_code <> :unfiled_code
            ORDER BY created_at ASC
            LIMIT 1
            """
        ),
        {"unfiled_code": UNFILED_CODE},
    ).scalar()

    # Ensure the global Unfiled study exists (keyed by its code for idempotency).
    unfiled_id_raw = conn.execute(
        sa.text("SELECT id FROM investigations WHERE investigation_code = :code"),
        {"code": UNFILED_CODE},
    ).scalar()
    unfiled_created = False
    if unfiled_id_raw is None:
        # Mint the id in Python (no DB-side default / ``RETURNING``); ``.hex``
        # fits the ``CHAR(32)`` column.
        new_unfiled = uuid.uuid4()
        conn.execute(
            sa.text(
                """
                INSERT INTO investigations
                    (id, investigation_id, investigation_code, title, description, status)
                VALUES
                    (:id, :pub, :code, :title, :description, 'active')
                """
            ),
            {
                "id": new_unfiled.hex,
                "pub": new_public_id(PublicIdPrefix.INVESTIGATION),
                "code": UNFILED_CODE,
                "title": UNFILED_TITLE,
                "description": UNFILED_DESCRIPTION,
            },
        )
        unfiled_id = new_unfiled.hex
        unfiled_created = True
    else:
        unfiled_id = _uuid_hex(unfiled_id_raw)

    # Keep the demo study's members: experiments whose lesson was in its scope.
    # Skipped if the join table is already gone (re-run after part B, and always
    # under the squashed baseline which never creates it). ``has_table`` is the
    # existence check.
    filed_into_demo = 0
    join_table_exists = sa.inspect(conn).has_table("investigation_lessons")
    if demo_id is not None and join_table_exists:
        filed_into_demo = conn.execute(
            sa.text(
                """
                UPDATE experiments e
                SET investigation_db_id = :demo
                WHERE e.investigation_db_id IS NULL
                  AND e.lesson_period_id IS NOT NULL
                  AND EXISTS (
                      SELECT 1 FROM investigation_lessons il
                      WHERE il.investigation_db_id = :demo
                        AND il.lesson_period_id = e.lesson_period_id
                  )
                """
            ),
            {"demo": demo_id},
        ).rowcount

    # Everything still unparented goes to Unfiled.
    filed_into_unfiled = conn.execute(
        sa.text(
            "UPDATE experiments SET investigation_db_id = :unfiled "
            "WHERE investigation_db_id IS NULL"
        ),
        {"unfiled": unfiled_id},
    ).rowcount

    residual = conn.execute(
        sa.text("SELECT count(*) FROM experiments WHERE investigation_db_id IS NULL")
    ).scalar_one()

    return _BackfillReport(
        unfiled_created=unfiled_created,
        filed_into_demo=int(filed_into_demo),
        filed_into_unfiled=int(filed_into_unfiled),
        residual_null=int(residual),
    )
