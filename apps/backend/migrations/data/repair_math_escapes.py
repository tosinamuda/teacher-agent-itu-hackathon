r"""Repair LaTeX commands corrupted by a math-blind escape-decode.

An earlier ``decode_llm_json_escapes`` only treated ``$…$`` as math, so the
LaTeX-style ``\(…\)`` / ``\[…\]`` runs the LLM actually emits were decoded as
ordinary text: ``\frac`` became form-feed + ``rac``, ``\times`` became tab +
``imes``. Those control characters were written into ``artefacts.manifest``
(review-pack block ``content`` / visual ``caption``) and
``evaluation_audit_items`` excerpts, so KaTeX/MathJax sees broken commands.

The generation seam + ``app/shared/llm_text.py`` are now math-aware, so new
content ships clean. This module back-populates: walk the stored rows and, inside
math runs only, convert the stray control characters back to ``\f`` / ``\t`` /
… (``repair_math_control_chars``). Idempotent — clean rows are a no-op.

CLI: ``uv run python -m migrations.data.repair_math_escapes``.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from typing import Any, cast

import sqlalchemy as sa

from app.db.config import get_sync_database_url
from app.shared.json_types import JsonObject
from app.shared.llm_text import repair_math_control_chars


def _repair_block(block: JsonObject) -> tuple[JsonObject, bool]:
    """Repair math control chars in a single review-pack block's text fields."""
    changed = False
    out = deepcopy(block)
    for field in ("content", "caption"):
        value = out.get(field)
        if isinstance(value, str) and value:
            repaired = repair_math_control_chars(value)
            if repaired != value:
                out[field] = repaired
                changed = True
    return out, changed


def _repair_manifest(manifest: JsonObject) -> tuple[JsonObject, int]:
    """Repair every block in a PostClassReviewPack manifest; return (manifest, n)."""
    changed = 0
    out = deepcopy(manifest)
    steps_raw = out.get("steps")
    if not isinstance(steps_raw, list):
        return out, 0
    new_steps: list[Any] = []
    for step in steps_raw:
        if not isinstance(step, dict):
            new_steps.append(step)
            continue
        step_out = deepcopy(cast(JsonObject, step))
        blocks_raw = step_out.get("blocks")
        if isinstance(blocks_raw, list):
            new_blocks: list[Any] = []
            for block in blocks_raw:
                if isinstance(block, dict):
                    cleaned, block_changed = _repair_block(cast(JsonObject, block))
                    if block_changed:
                        changed += 1
                    new_blocks.append(cleaned)
                else:
                    new_blocks.append(block)
            step_out["blocks"] = new_blocks
        new_steps.append(step_out)
    out["steps"] = new_steps
    return out, changed


def apply_artefact_manifest_repair(connection: sa.Connection) -> dict[str, int]:
    """Walk artefacts, repair math control chars in each manifest, write back.

    Idempotent. Returns ``{"scanned": N, "updated": K, "blocks_changed": B}``.
    """
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


def apply_audit_item_repair(connection: sa.Connection) -> dict[str, int]:
    """Repair math control chars in evaluation_audit_items text fields. Idempotent."""
    rows = connection.execute(
        sa.text(
            "SELECT id, generated_excerpt, source_excerpt, figure_caption "
            "FROM evaluation_audit_items"
        )
    ).all()
    scanned = 0
    updated = 0
    for row in rows:
        scanned += 1
        new_values: dict[str, str] = {}
        for field, value in (
            ("generated_excerpt", row.generated_excerpt),
            ("source_excerpt", row.source_excerpt),
            ("figure_caption", row.figure_caption),
        ):
            if isinstance(value, str) and value:
                repaired = repair_math_control_chars(value)
                if repaired != value:
                    new_values[field] = repaired
        if not new_values:
            continue
        set_clause = ", ".join(f"{name} = :{name}" for name in new_values)
        connection.execute(
            sa.text(f"UPDATE evaluation_audit_items SET {set_clause} WHERE id = :id"),
            {**new_values, "id": row.id},
        )
        updated += 1
    return {"scanned": scanned, "updated": updated}


def run(database_url: str | None = None) -> dict[str, dict[str, int]]:
    """Apply both repair passes to a database and return summary stats."""
    url = database_url or get_sync_database_url()
    engine = sa.create_engine(url, future=True)
    with engine.begin() as conn:
        artefact_stats = apply_artefact_manifest_repair(conn)
        audit_stats = apply_audit_item_repair(conn)
    return {"artefacts": artefact_stats, "audit_items": audit_stats}


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", default=None, help="Database URL override.")
    args = parser.parse_args()
    print(json.dumps(run(args.database_url), indent=2))


if __name__ == "__main__":
    _main()
