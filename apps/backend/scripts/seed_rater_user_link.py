"""Pair human raters in ``evaluation_raters`` to ``users`` (role='rater').

Invocation::

    uv run python -m scripts.seed_rater_user_link

Idempotent. Run AFTER the ``20260609_rater_user_link`` migration adds the
``evaluation_raters.user_id`` column. Synthetic judges (display_name starting
with "Synthetic Judge") are skipped — only human raters get a User identity.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.rater_user_link import link_raters_to_users


def main() -> int:
    with sync_engine.begin() as conn:
        result = link_raters_to_users(conn)
    print("rater→user link complete:")
    print(f"  raters_scanned           = {result.raters_scanned}")
    print(f"  raters_already_linked    = {result.raters_already_linked}")
    print(f"  raters_linked            = {result.raters_linked}")
    print(f"  raters_synthetic_skipped = {result.raters_synthetic_skipped}")
    print(f"  raters_collision_skipped = {result.raters_collision_skipped}")
    print(f"  users_created            = {result.users_created}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
