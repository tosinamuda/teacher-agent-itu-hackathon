"""Seed Casbin capability policies + role grants from the users table.

Invocation::

    uv run python -m scripts.seed_casbin_policies

Idempotent. Run AFTER the ``20260609_casbin_rule_table`` migration creates the
storage table, and AFTER user identities (research_manager / teacher) exist in
the ``users`` table. Safe to re-run any time — it adds missing rows only.
"""

from __future__ import annotations

import sys

from app.db.session import sync_engine
from migrations.data.casbin_policy_seed import seed_casbin_policies


def main() -> int:
    with sync_engine.begin() as conn:
        result = seed_casbin_policies(conn)
    print("casbin policy seed complete:")
    print(f"  capabilities_added = {result.capabilities_added}")
    print(f"  grants_added       = {result.grants_added}")
    print(f"  capabilities_total = {result.capabilities_total}")
    print(f"  grants_total       = {result.grants_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
