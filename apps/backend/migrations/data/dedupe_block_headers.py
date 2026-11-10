r"""Remove duplicate block headers from existing review-note manifests.

The manifest adapter used to always prepend a generic kind label
(``**Worked example**`` / ``**Practice**`` / ``**Reflection**``) to a block's
text, even when the generated text already opened with its own heading — so the
two stacked into a duplicate header:

    **Worked example**

    **Worked Example**

    Find an equivalent fraction for …

The adapter now skips the generic label when the text has its own heading. This
module back-fixes stored manifests: where a block's ``content`` starts with one
of the generic labels *and* the remainder starts with another heading
(``**`` / ``#``), drop the redundant generic label. Idempotent — already-clean
content is a no-op.

CLI: ``uv run python -m migrations.data.dedupe_block_headers``.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from typing import cast

import sqlalchemy as sa

from app.db.config import get_sync_database_url
from app.shared.json_types import JsonObject

_GENERIC_LABELS = (
    "**Worked example**\n\n",
    "**Practice**\n\n",
    "**Reflection**\n\n",
)


def _dedupe(content: str) -> str:
    """Drop a leading generic label when the rest opens with its own heading."""
    for label in _GENERIC_LABELS:
        if content.startswith(label):
            rest = content[len(label) :]
            if rest.lstrip().startswith(("**", "#")):
                return rest
    return content


def _repair_manifest(manifest: JsonObject) -> tuple[JsonObject, int]:
    """Dedupe headers in every explanation block of a manifest; return (manifest, n)."""
    out = deepcopy(manifest)
    steps_raw = out.get("steps")
    if not isinstance(steps_raw, list):
        return out, 0
    changed = 0
    for step in steps_raw:
        if not isinstance(step, dict):
            continue
        blocks_raw = step.get("blocks")
        if not isinstance(blocks_raw, list):
            continue
        for block in blocks_raw:
            if not isinstance(block, dict):
                continue
            content = block.get("content")
            if isinstance(content, str) and content:
                deduped = _dedupe(content)
                if deduped != content:
                    block["content"] = deduped
                    changed += 1
    return out, changed


def apply_header_dedupe(connection: sa.Connection) -> dict[str, int]:
    """Walk artefacts, dedupe duplicate block headers, write back. Idempotent."""
    rows = connection.execute(
        sa.text("SELECT id, manifest FROM artefacts WHERE manifest IS NOT NULL")
    ).all()
    scanned = 0
    updated = 0
    blocks_changed_total = 0
    for row in rows:
        scanned += 1
        manifest_raw = row.manifest
        if isinstance(manifest_raw, str):
            manifest_raw = json.loads(manifest_raw)
        if not isinstance(manifest_raw, dict):
            continue
        cleaned, blocks_changed = _repair_manifest(cast(JsonObject, manifest_raw))
        if blocks_changed == 0:
            continue
        connection.execute(
            sa.text("UPDATE artefacts SET manifest = CAST(:m AS JSON) WHERE id = :id"),
            {"m": json.dumps(cleaned), "id": row.id},
        )
        updated += 1
        blocks_changed_total += blocks_changed
    return {"scanned": scanned, "updated": updated, "blocks_changed": blocks_changed_total}


def run(database_url: str | None = None) -> dict[str, int]:
    """Apply the header-dedupe pass to a database and return summary stats."""
    url = database_url or get_sync_database_url()
    engine = sa.create_engine(url, future=True)
    with engine.begin() as conn:
        return apply_header_dedupe(conn)


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", default=None, help="Database URL override.")
    args = parser.parse_args()
    print(json.dumps(run(args.database_url), indent=2))


if __name__ == "__main__":
    _main()
