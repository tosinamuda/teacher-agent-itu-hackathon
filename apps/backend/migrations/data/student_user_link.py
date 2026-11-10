"""Pair students with a ``code`` to ``users`` rows (Phase F of the RBAC redesign).

For each ``student_profiles`` row that has a non-NULL ``code``, ensure a User
exists (auth_id = ``code|student-{code}``, role='student') and the FK
``student_profiles.user_id`` points at it. Students without a ``code`` are
research-only synthetic identities — they stay ``user_id IS NULL``.

Idempotent: an already-linked profile is left alone; a missing User is created;
a slug collision (two ``code`` values that sanitise the same) is reported and
skipped rather than crashing.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import sqlalchemy as sa


def _uuid_hex(value: object) -> str:
    """Normalise a raw-SQL uuid value to 32-char hex (no dashes).

    A uuid read via raw ``sa.text`` bypasses the ORM ``Uuid`` type, so it comes
    back as the bare ``CHAR(32)`` hex MySQL stores. ``uuid.UUID`` parses it and
    ``.hex`` is the canonical 32-char form to bind back into the column.
    """
    return uuid.UUID(str(value)).hex


@dataclass(frozen=True)
class _LinkReport:
    students_scanned: int
    students_already_linked: int
    students_linked: int
    students_no_code: int
    students_collision_skipped: int
    users_created: int


def _ensure_user_row(
    conn: sa.Connection, *, auth_id: str, email: str, full_name: str
) -> tuple[str, bool]:
    """Return ``(users.id, created)`` — find or insert the student-role user row."""
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
            "VALUES (:id, :aid, :email, :name, 'student')"
        ),
        {"id": new_id.hex, "aid": auth_id, "email": email, "name": full_name},
    )
    return new_id.hex, True


def link_students_to_users(conn: sa.Connection) -> _LinkReport:
    """Link every student with a non-NULL ``code`` to a users row."""
    student_rows = conn.execute(
        sa.text(
            "SELECT id, student_id, full_name, code, user_id "
            "FROM student_profiles ORDER BY created_at"
        )
    ).all()

    students_scanned = len(student_rows)
    students_already_linked = 0
    students_linked = 0
    students_no_code = 0
    students_collision_skipped = 0
    users_created = 0

    bound_user_ids: set[str] = {
        _uuid_hex(uid)
        for (uid,) in conn.execute(
            sa.text("SELECT user_id FROM student_profiles WHERE user_id IS NOT NULL")
        ).all()
    }

    for student_pk_raw, _student_pub_id, full_name, code, current_user_id in student_rows:
        if current_user_id is not None:
            students_already_linked += 1
            continue
        if not code:
            students_no_code += 1
            continue
        auth_id = f"code|student-{code}"
        email = f"student-{code}@school.com"
        user_id, created = _ensure_user_row(conn, auth_id=auth_id, email=email, full_name=full_name)
        if user_id in bound_user_ids:
            students_collision_skipped += 1
            continue
        if created:
            users_created += 1
        conn.execute(
            sa.text("UPDATE student_profiles SET user_id = :uid WHERE id = :pk"),
            {"uid": user_id, "pk": _uuid_hex(student_pk_raw)},
        )
        bound_user_ids.add(user_id)
        students_linked += 1

    return _LinkReport(
        students_scanned=students_scanned,
        students_already_linked=students_already_linked,
        students_linked=students_linked,
        students_no_code=students_no_code,
        students_collision_skipped=students_collision_skipped,
        users_created=users_created,
    )
