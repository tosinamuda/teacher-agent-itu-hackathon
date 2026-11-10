"""Asset manifest + resolver: the source assets a step may place, by stable ref id.

The LLM is given the manifest (ref_id + the figure's REAL vision caption) and references
assets by id; the resolver turns a ref id into the verbatim, provenance-tagged source block
(figures carry their caption as a figcaption). The LLM never sees or emits the asset content
— only its id and caption.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from app.shared.json_types import JsonObject
from experiments.source_transclusion.transclude import extract_display_math


@dataclass
class Asset:
    ref_id: str
    kind: str  # "table" | "figure"
    description: str
    block: JsonObject  # the verbatim, provenance-tagged content block


def _image_assets(record: JsonObject) -> list[JsonObject]:
    raw = record.get("asset_refs")
    if not isinstance(raw, list):
        return []
    return [
        cast(JsonObject, a)
        for a in raw
        if isinstance(a, dict) and a.get("asset_type") == "image" and a.get("src")
    ]


def build_manifest(record: JsonObject) -> list[Asset]:
    """Build the placeable-asset manifest for one grounding record (figures use real captions)."""
    record_id = str(record.get("record_id") or "rec")
    content_text = str(record.get("content_text") or "")
    assets: list[Asset] = []

    for index, array in enumerate(extract_display_math(content_text), 1):
        ref_id = f"{record_id}:table{index}"
        assets.append(
            Asset(
                ref_id=ref_id,
                kind="table",
                description=f"A reference table from the textbook ({record_id}), shown as LaTeX.",
                block={
                    "id": ref_id,
                    "type": "explanation",
                    "content": f"$$\n{array}\n$$",
                    "source_record_id": record_id,
                    "transcluded": True,
                },
            )
        )
    for index, asset in enumerate(_image_assets(record), 1):
        ref_id = f"{record_id}:fig{index}"
        caption = str(asset.get("caption") or "").strip()
        assets.append(
            Asset(
                ref_id=ref_id,
                kind="figure",
                description=caption or f"Figure {index} from {record_id} (no caption available).",
                block={
                    "id": ref_id,
                    "type": "visual",
                    "variant": "image",
                    "url": str(asset["src"]),
                    "caption": caption or None,  # transcluded figcaption
                    "source_record_id": record_id,
                    "transcluded": True,
                },
            )
        )
    return assets


def manifest_text(assets: list[Asset]) -> str:
    """The manifest as the LLM sees it: one `ref_id — caption/description` line per asset."""
    return "\n".join(f"{asset.ref_id} — {asset.description}" for asset in assets)


def resolve(ref_id: str, assets: list[Asset]) -> JsonObject | None:
    """Return the verbatim block for a ref id, or None if the id is not in the manifest."""
    for asset in assets:
        if asset.ref_id == ref_id:
            return dict(asset.block)
    return None
