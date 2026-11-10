from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import cast

from app.shared.json_types import JsonObject


def _dict_list(value: object) -> list[JsonObject]:
    """List narrowing; ``[]`` if not a list. Local replacement for ``as_object_list``."""
    return cast(list[JsonObject], value) if isinstance(value, list) else []


def _object_dict(value: object) -> JsonObject | None:
    if not isinstance(value, dict):
        return None
    return cast(JsonObject, value)


def textbook_record_id(record: object) -> str:
    if isinstance(record, dict):
        record_payload = cast(JsonObject, record)
        return str(
            record_payload.get("record_id") or record_payload.get("section_ref") or ""
        ).strip()
    return str(
        getattr(record, "record_id", None) or getattr(record, "section_ref", None) or ""
    ).strip()


def normalize_textbook_records(
    reference_context: Sequence[Mapping[str, object]],
) -> list[JsonObject]:
    normalized: list[JsonObject] = []
    for record in reference_context:
        if record.get("type") != "textbook_record":
            continue
        cloned = cast(JsonObject, deepcopy(dict(record)))
        record_id = textbook_record_id(cloned)
        if not record_id:
            continue
        cloned["record_id"] = record_id
        normalized.append(cloned)
    return normalized


def build_record_catalog(textbook_records: list[JsonObject]) -> list[JsonObject]:
    catalog: list[JsonObject] = []
    for record in textbook_records:
        record_id = textbook_record_id(record)
        if not record_id:
            continue
        catalog.append(
            {
                "record_id": record_id,
                "title": str(record.get("title") or "").strip(),
                "record_type": str(record.get("record_type") or "").strip() or None,
                "section_ref": str(record.get("section_ref") or "").strip() or None,
                "source_html_path": str(record.get("source_html_path") or "").strip() or None,
                "source_anchor_id": str(record.get("source_anchor_id") or "").strip() or None,
                "has_image_asset": any(
                    asset is not None
                    and str(asset.get("asset_type") or "").strip() == "image"
                    and str(asset.get("src") or "").strip()
                    for raw_asset in _dict_list(record.get("asset_refs"))
                    for asset in [_object_dict(raw_asset)]
                ),
            }
        )
    return catalog


def derive_textbook_references(
    evidence_summaries: list[JsonObject],
    textbook_records: list[JsonObject],
) -> list[str]:
    seen: set[tuple[str, str]] = set()
    references: list[str] = []

    for summary in evidence_summaries:
        for raw_record in _dict_list(summary.get("records")):
            record = _object_dict(raw_record)
            if record is None:
                continue
            title = str(record.get("title") or "").strip()
            section_ref = str(record.get("section_ref") or "").strip()
            if not title or not section_ref:
                continue
            key = (title, section_ref)
            if key in seen:
                continue
            seen.add(key)
            references.append(f"{title} ({section_ref})")

    if references:
        return references

    for record in textbook_records:
        title = str(record.get("title") or "").strip()
        section_ref = str(record.get("section_ref") or "").strip()
        if not title or not section_ref:
            continue
        key = (title, section_ref)
        if key in seen:
            continue
        seen.add(key)
        references.append(f"{title} ({section_ref})")

    return references
