"""Deterministic transclusion: build content blocks from a source record, verbatim.

No LLM. The display-math arrays and image figures are lifted straight from the grounding
record, so their LaTeX is exactly as authored (valid) and their content is exactly the
source (faithful). Every block is provenance-tagged with its `source_record_id` by
construction — the audit link the regeneration path never carried.
"""

from __future__ import annotations

import re

from app.shared.json_types import JsonObject

_ARRAY = re.compile(r"\\begin\{array\}.*?\\end\{array\}", re.DOTALL)
_IMAGE_MD = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def extract_display_math(content_text: str) -> list[str]:
    """Verbatim display-math arrays from a record's content_text — valid as authored."""
    return [match.group(0).strip() for match in _ARRAY.finditer(content_text or "")]


def extract_image_urls(record: JsonObject) -> list[str]:
    """Image urls for the record, from asset_refs first, then content_text markdown."""
    urls: list[str] = []
    raw_assets = record.get("asset_refs")
    for asset in raw_assets if isinstance(raw_assets, list) else []:
        if isinstance(asset, dict) and asset.get("asset_type") == "image" and asset.get("src"):
            urls.append(str(asset["src"]))
    for match in _IMAGE_MD.finditer(str(record.get("content_text") or "")):
        if match.group(1) not in urls:
            urls.append(match.group(1))
    return urls


def source_blocks(record: JsonObject, *, step_id: str) -> list[JsonObject]:
    """Verbatim, provenance-tagged content blocks transcluded from one source record."""
    record_id = str(record.get("record_id") or "rec")
    blocks: list[JsonObject] = []

    for index, array in enumerate(extract_display_math(str(record.get("content_text") or "")), 1):
        blocks.append(
            {
                "id": f"{step_id}-src-{record_id}-math{index}",
                "type": "explanation",
                "content": f"$$\n{array}\n$$",
                "source_record_id": record_id,  # provenance by construction
                "transcluded": True,
            }
        )
    for index, url in enumerate(extract_image_urls(record), 1):
        blocks.append(
            {
                "id": f"{step_id}-src-{record_id}-fig{index}",
                "type": "visual",
                "variant": "image",
                "url": url,
                "source_record_id": record_id,
                "transcluded": True,
            }
        )
    return blocks


def assemble_step(
    *,
    step_id: str,
    title: str,
    prose_markdown: str,
    grounded_records: list[JsonObject],
) -> JsonObject:
    """A step = the LLM's prose block, then the verbatim source assets spliced after it."""
    blocks: list[JsonObject] = [
        {"id": f"{step_id}-prose", "type": "explanation", "content": prose_markdown}
    ]
    for record in grounded_records:
        blocks.extend(source_blocks(record, step_id=step_id))
    return {"step_id": step_id, "step_kind": "core", "title": title, "blocks": blocks}
