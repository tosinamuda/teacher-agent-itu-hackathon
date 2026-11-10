"""De-dup casbin_rule + enforce unique policies (defense-in-depth).

``casbin_rule`` (the adapter's policy table) has no unique constraint, so a grant
that races the enforcer's in-memory check could persist a duplicate
``g, user, role`` row. A plain unique index can't dedupe it: ``v0``–``v5`` are
nullable and g-rows leave ``v2``–``v5`` NULL, which MySQL treats as distinct.

We add a STORED generated column holding the NULL-coalesced policy tuple and make
it unique. A hash (MD5/SHA) would be ideal for a fixed-width key, but MySQL
disallows those functions in generated columns — so we index the tuple itself via
a 700-char prefix (2800 bytes, within InnoDB's 3072-byte limit). Real casbin
policies (roles, uuids, ``obj:act`` patterns) are far shorter than 700 chars, so
the prefix covers them in full and dedupes exactly.

Not currently reachable via the app (``grant_role_to_user`` runs once per onboard and
onboarding dedupes the user), so this is defense-in-depth + a data-integrity
invariant on the policy table. MySQL-specific (generated column). Tests build the
schema via ``create_all``, which doesn't manage ``casbin_rule`` — verified against
the dev DB, not the create_all test DB.

Revision ID: 0004_casbin_rule_unique
Revises: 0003_revision_uniqueness
Create Date: 2026-06-17
"""

from __future__ import annotations

from alembic import op

revision = "0004_casbin_rule_unique"
down_revision = "0003_revision_uniqueness"
branch_labels = None
depends_on = None

# CHAR(31) = ASCII unit separator: a byte that can't appear in a policy value, so the
# joined tuple can't collide across column boundaries.
_POLICY_KEY = (
    "CONCAT_WS(CHAR(31), COALESCE(ptype,''), COALESCE(v0,''), COALESCE(v1,''), "
    "COALESCE(v2,''), COALESCE(v3,''), COALESCE(v4,''), COALESCE(v5,''))"
)


def upgrade() -> None:
    # 1) Drop any pre-existing duplicate policy rows, keeping the lowest id. ``<=>`` is
    #    NULL-safe equality so g-rows with NULL v2–v5 compare as equal.
    op.execute(
        """
        DELETE c1 FROM casbin_rule c1
        JOIN casbin_rule c2
          ON c1.id > c2.id
         AND c1.ptype <=> c2.ptype
         AND c1.v0 <=> c2.v0 AND c1.v1 <=> c2.v1 AND c1.v2 <=> c2.v2
         AND c1.v3 <=> c2.v3 AND c1.v4 <=> c2.v4 AND c1.v5 <=> c2.v5
        """
    )
    # 2) A STORED column holding the full NULL-coalesced policy tuple, made unique on a
    #    700-char prefix (covers every real policy; within the index byte limit).
    op.execute(
        f"ALTER TABLE casbin_rule "
        f"ADD COLUMN policy_key VARCHAR(1791) GENERATED ALWAYS AS ({_POLICY_KEY}) STORED, "
        f"ADD UNIQUE KEY uq_casbin_rule_policy (policy_key(700))"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE casbin_rule DROP INDEX uq_casbin_rule_policy")
    op.execute("ALTER TABLE casbin_rule DROP COLUMN policy_key")
