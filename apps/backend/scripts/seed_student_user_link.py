"""Pair students (those with a ``code``) to ``users`` rows.

Invocation::

    uv run python -m scripts.seed_student_user_link

Idempotent. Run AFTER the ``20260609_student_user_link`` migration adds the
``student_profiles.user_id`` column. Students with no ``code`` (pure research
synthetic identities) are skipped.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.student_user_link import link_students_to_users


def main() -> int:
    with sync_engine.begin() as conn:
        result = link_students_to_users(conn)
    print("student→user link complete:")
    print(f"  students_scanned            = {result.students_scanned}")
    print(f"  students_already_linked     = {result.students_already_linked}")
    print(f"  students_linked             = {result.students_linked}")
    print(f"  students_no_code            = {result.students_no_code}")
    print(f"  students_collision_skipped  = {result.students_collision_skipped}")
    print(f"  users_created               = {result.users_created}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
