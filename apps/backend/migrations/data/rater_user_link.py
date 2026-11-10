"""Pair human raters to ``users`` rows (Phase E of the RBAC redesign).

For each ``evaluation_raters`` row that looks human (display_name doesn't start
with "Synthetic Judge"), ensure a matching ``users`` row exists with
role='rater' and the FK ``evaluation_raters.user_id`` points at it. Synthetic
judges are skipped — they remain ``user_id IS NULL``.

Idempotent: existing user_id links are left alone; an unpaired human rater
gets a new user (auth_id = ``code|rater-<sanitised-display-name>``) or links to
an existing rater-role user with that auth_id if one is already present.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass

import sqlalchemy as sa


def _uuid_hex(value: object) -> str:
    """Normalise a raw-SQL uuid value to 32-char hex (no dashes).

    Reading a uuid via raw ``sa.text`` bypasses the ORM ``Uuid`` type, so it
    comes back as the bare ``CHAR(32)`` hex MySQL stores. ``uuid.UUID`` parses it
    and ``.hex`` is the canonical 32-char form to bind back into the column.
    """
    return uuid.UUID(str(value)).hex


# Names that pattern as programmatic identities, not human logins. ``Synthetic
# Judge`` is the dominant pattern; ``Synthetic Source Auditor`` exists too.
_SYNTHETIC_PREFIX = "Synthetic"


@dataclass(frozen=True)
class _LinkReport:
    raters_scanned: int
    raters_already_linked: int
    raters_linked: int
    raters_synthetic_skipped: int
    raters_collision_skipped: int
    users_created: int


def _slug(display_name: str) -> str:
    """``Tosin Owolabi`` → ``tosin-owolabi``. Lowercased, non-alphanum collapsed."""
    return re.sub(r"[^a-z0-9]+", "-", display_name.lower()).strip("-") or "rater"


def _ensure_user_row(
    conn: sa.Connection, *, auth_id: str, email: str, full_name: str
) -> tuple[str, bool]:
    """Return ``(users.id, created)`` — find or insert the rater-role user row."""
    existing = conn.execute(
        sa.text("SELECT id FROM users WHERE auth_id = :aid"),
        {"aid": auth_id},
    ).scalar()
    if existing is not None:
        return _uuid_hex(existing), False
    # Mint the id in Python (no DB-side default / ``RETURNING``); ``.hex`` fits
    # the ``CHAR(32)`` column.
    new_id = uuid.uuid4()
    conn.execute(
        sa.text(
            "INSERT INTO users (id, auth_id, email, full_name, role) "
            "VALUES (:id, :aid, :email, :name, 'rater')"
        ),
        {"id": new_id.hex, "aid": auth_id, "email": email, "name": full_name},
    )
    return new_id.hex, True


def link_raters_to_users(conn: sa.Connection) -> _LinkReport:
    """Link every human rater to a users row; skip synthetic judges."""
    rater_rows = conn.execute(
        sa.text(
            "SELECT id, rater_id, display_name, user_id FROM evaluation_raters ORDER BY created_at"
        )
    ).all()

    raters_scanned = len(rater_rows)
    raters_already_linked = 0
    raters_linked = 0
    raters_synthetic_skipped = 0
    raters_collision_skipped = 0
    users_created = 0

    # Track which user rows are already taken in this pass so we don't try to
    # bind two raters to the same login (would hit the UNIQUE(user_id) FK).
    bound_user_ids: set[str] = {
        _uuid_hex(uid)
        for (uid,) in conn.execute(
            sa.text("SELECT user_id FROM evaluation_raters WHERE user_id IS NOT NULL")
        ).all()
    }

    for rater_pk_raw, _rater_pub_id, display_name, current_user_id in rater_rows:
        if current_user_id is not None:
            raters_already_linked += 1
            continue
        if display_name.startswith(_SYNTHETIC_PREFIX):
            raters_synthetic_skipped += 1
            continue

        slug = _slug(display_name)
        auth_id = f"code|rater-{slug}"
        email = f"rater-{slug}@school.com"
        user_id, created = _ensure_user_row(
            conn, auth_id=auth_id, email=email, full_name=display_name
        )
        if user_id in bound_user_ids:
            # Two raters slug to the same auth_id ("Tosin" + "tosin") — the
            # first one wins the link; the rest stay user_id=NULL and can be
            # re-bound manually if they represent distinct humans.
            raters_collision_skipped += 1
            continue
        if created:
            users_created += 1
        conn.execute(
            sa.text("UPDATE evaluation_raters SET user_id = :uid WHERE id = :pk"),
            {"uid": user_id, "pk": _uuid_hex(rater_pk_raw)},
        )
        bound_user_ids.add(user_id)
        raters_linked += 1

    return _LinkReport(
        raters_scanned=raters_scanned,
        raters_already_linked=raters_already_linked,
        raters_linked=raters_linked,
        raters_synthetic_skipped=raters_synthetic_skipped,
        raters_collision_skipped=raters_collision_skipped,
        users_created=users_created,
    )
