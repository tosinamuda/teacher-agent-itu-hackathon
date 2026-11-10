r"""Decode JSON-style escape sequences left in already-stored LLM content.

The LLM occasionally emits text fields as JSON-encoded literals — backslash +
``n`` instead of an actual newline, ``\u20XX`` instead of the codepoint, and
so on — when its prompt format steered it toward a JSON shape. Those
escapes survive into ``artefacts.manifest`` (review-pack block ``content``
/ visual ``caption``) and into ``evaluation_audit_items.generated_excerpt``,
where the markdown converter prints them verbatim and raters see
``\n\n`` mid-paragraph.

The generation seam is now patched in
``app/domains/experiments/study_pack/section/assembly.py::normalise_section`` so
all new packs ship clean. This module handles the back-population: walk the
existing rows, decode JSON escapes outside math regions
(``decode_llm_json_escapes`` from ``app/shared/llm_text.py``), and write the
cleaned text back. Idempotent — re-running on already-clean rows is a no-op.

CLI: ``uv run python -m migrations.data.llm_text_decode_existing``.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from typing import Any, cast

import sqlalchemy as sa

from app.db.config import get_sync_database_url
from app.shared.json_types import JsonObject
from app.shared.llm_text import decode_llm_json_escapes


def _decode_block(block: JsonObject) -> tuple[JsonObject, bool]:
    """Decode JSON escapes in a single review-pack block.

    Returns the (possibly cleaned) block plus a ``changed`` flag. Only the
    ``content`` (explanation text) and ``caption`` (visual figure caption)
    fields are touched; everything else is passed through unchanged.
    """
    changed = False
    out = deepcopy(block)
    for field in ("content", "caption"):
        value = out.get(field)
        if isinstance(value, str) and value:
            decoded = decode_llm_json_escapes(value)
            if decoded != value:
                out[field] = decoded
                changed = True
    return out, changed


def _decode_manifest(manifest: JsonObject) -> tuple[JsonObject, int]:
    """Decode every block in a PostClassReviewPack manifest in place.

    Returns the new manifest plus the number of blocks whose text changed.
    """
    changed = 0
    out = deepcopy(manifest)
    steps_raw = out.get("steps")
    if not isinstance(steps_raw, list):
        return out, 0
    new_steps: list[JsonObject] = []
    for step in steps_raw:
        if not isinstance(step, dict):
            new_steps.append(cast(JsonObject, step))
            continue
        step_out = deepcopy(cast(JsonObject, step))
        blocks_raw = step_out.get("blocks")
        if isinstance(blocks_raw, list):
            new_blocks: list[Any] = []
            for block in blocks_raw:
                if isinstance(block, dict):
                    cleaned, block_changed = _decode_block(cast(JsonObject, block))
                    if block_changed:
                        changed += 1
                    new_blocks.append(cleaned)
                else:
                    new_blocks.append(block)
            step_out["blocks"] = new_blocks
        new_steps.append(step_out)
    out["steps"] = new_steps
    return out, changed


def apply_artefact_manifest_decoding(connection: sa.Connection) -> dict[str, int]:
    """Walk artefacts, decode JSON escapes in each manifest, write changes back.

    Idempotent — manifests already clean (whose decoded text equals the
    stored text) are not rewritten. Returns ``{"scanned": N, "updated": K,
    "blocks_changed": B}``.
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
        cleaned, blocks_changed = _decode_manifest(cast(JsonObject, manifest_raw))
        if blocks_changed == 0:
            continue
        connection.execute(
            sa.text("UPDATE artefacts SET manifest = CAST(:m AS JSON) WHERE id = :id"),
            {"m": json.dumps(cleaned), "id": row.id},
        )
        updated += 1
        blocks_changed_total += blocks_changed
    return {"scanned": scanned, "updated": updated, "blocks_changed": blocks_changed_total}


def apply_audit_item_decoding(connection: sa.Connection) -> dict[str, int]:
    """Decode JSON escapes in evaluation_audit_items.generated_excerpt + figure_caption.

    Idempotent. Returns ``{"scanned": N, "updated": K}``.
    """
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
        new_values: dict[str, str | None] = {}
        for field, value in (
            ("generated_excerpt", row.generated_excerpt),
            ("source_excerpt", row.source_excerpt),
            ("figure_caption", row.figure_caption),
        ):
            if isinstance(value, str) and value:
                decoded = decode_llm_json_escapes(value)
                if decoded != value:
                    new_values[field] = decoded
        if not new_values:
            continue
        # Build the UPDATE dynamically so untouched fields stay untouched.
        set_clause = ", ".join(f"{name} = :{name}" for name in new_values)
        connection.execute(
            sa.text(f"UPDATE evaluation_audit_items SET {set_clause} WHERE id = :id"),
            {**new_values, "id": row.id},
        )
        updated += 1
    return {"scanned": scanned, "updated": updated}


def run(database_url: str | None = None) -> dict[str, dict[str, int]]:
    """Apply both decoding passes to a database and return summary stats."""
    url = database_url or get_sync_database_url()
    engine = sa.create_engine(url, future=True)
    with engine.begin() as conn:
        artefact_stats = apply_artefact_manifest_decoding(conn)
        audit_stats = apply_audit_item_decoding(conn)
    return {"artefacts": artefact_stats, "audit_items": audit_stats}


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database-url",
        default=None,
        help="Database URL override (defaults to CONFIG.database_url).",
    )
    args = parser.parse_args()
    stats = run(args.database_url)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    _main()
