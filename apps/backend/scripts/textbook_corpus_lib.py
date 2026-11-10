"""Shared helpers for textbook corpus verification and seeding."""

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


def _default_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", _default_project_root()))
PROJECT_DATASET_ROOT = PROJECT_ROOT / "dataset" / "processed" / "textbook"
LINKED_ROOT = Path(os.getenv("TEXTBOOK_LINKED_ROOT", PROJECT_DATASET_ROOT / "jsonl" / "linked"))
CURRICULUM_PATH = Path(
    os.getenv(
        "CURRICULUM_PATH",
        PROJECT_ROOT / "dataset" / "processed" / "curriculum" / "jss1_topics_enriched.json",
    )
)
SCHEME_PATH = Path(
    os.getenv(
        "SCHEME_PATH",
        PROJECT_ROOT / "dataset" / "processed" / "scheme-of-work" / "jss1_scheme.json",
    )
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def linked_manifest_path() -> Path:
    return LINKED_ROOT / "manifest.json"


def linked_records_path() -> Path:
    return LINKED_ROOT / "records.jsonl"


def linked_subtopic_catalog_path() -> Path:
    return LINKED_ROOT / "subtopic_catalog.json"


def list_packet_paths() -> list[Path]:
    return sorted(LINKED_ROOT.glob("packet-*.json"))


def iter_packets(packet_id: str | None = None) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for path in list_packet_paths():
        packet = load_json(path)
        if packet_id and packet.get("packet_id") != packet_id:
            continue
        packet["_source_path"] = str(path)
        packets.append(packet)
    return packets


def iter_records(packet_id: str | None = None) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for packet in iter_packets(packet_id=packet_id):
        for record in packet.get("records") or []:
            records.append(record)
    return records


def curriculum_subtopic_ids() -> set[str]:
    topics = load_json(CURRICULUM_PATH)
    ids: set[str] = set()
    for topic in topics:
        for subtopic in topic.get("subtopics", []):
            subtopic_id = subtopic.get("subtopic_id")
            if isinstance(subtopic_id, str) and subtopic_id:
                ids.add(subtopic_id)
    return ids


def catalog_subtopic_ids() -> set[str]:
    catalog = load_json(linked_subtopic_catalog_path())
    if isinstance(catalog, list):
        rows = catalog
    else:
        rows = catalog.get("subtopics", [])
    return {
        row["subtopic_id"]
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("subtopic_id"), str)
    }


def verify_corpus(packet_id: str | None = None) -> dict[str, Any]:
    manifest = load_json(linked_manifest_path())
    packets = iter_packets(packet_id=packet_id)
    records_jsonl = load_jsonl(linked_records_path()) if packet_id is None else None
    curriculum_ids = curriculum_subtopic_ids()
    catalog_ids = catalog_subtopic_ids()

    packet_ids = [packet.get("packet_id") for packet in packets]
    duplicate_packet_ids = [item for item, count in Counter(packet_ids).items() if count > 1]

    record_ids: list[str] = []
    duplicate_record_ids: list[str] = []
    invalid_link_status_records: list[str] = []
    invalid_visibility_default_records: list[str] = []
    missing_retrieval_text_records: list[str] = []
    missing_primary_records: list[str] = []
    missing_subtopic_array_records: list[str] = []
    primary_not_in_links_records: list[str] = []
    missing_catalog_subtopics: set[str] = set()
    missing_curriculum_subtopics: set[str] = set()
    duplicate_record_subtopic_pairs: list[str] = []
    orphan_record_packet_refs: list[str] = []
    empty_packets: list[str] = []

    seen_record_subtopic_pairs: set[tuple[str, str]] = set()
    packet_record_counts: dict[str, int] = {}

    for packet in packets:
        current_packet_id = packet.get("packet_id")
        packet_records = packet.get("records") or []
        if isinstance(current_packet_id, str):
            packet_record_counts[current_packet_id] = len(packet_records)
        if not packet_records:
            empty_packets.append(str(current_packet_id))
        for record in packet_records:
            record_id = record.get("record_id")
            if isinstance(record_id, str):
                record_ids.append(record_id)
            else:
                continue

            if record.get("packet_id") not in (None, current_packet_id):
                orphan_record_packet_refs.append(record_id)

            link_status = record.get("link_status")
            if link_status not in {"linked", "ambiguous", "unlinked"}:
                invalid_link_status_records.append(record_id)

            retrieval_text = (record.get("retrieval_text") or "").strip()
            if not retrieval_text:
                missing_retrieval_text_records.append(record_id)

            visibility_default = record.get("visibility_default")
            if visibility_default not in {None, "visible", "hidden", "none"}:
                invalid_visibility_default_records.append(record_id)

            primary = record.get("primary_subtopic_id")
            subtopics = record.get("subtopic_ids") or []
            if not primary:
                missing_primary_records.append(record_id)
            if not isinstance(subtopics, list) or not subtopics:
                missing_subtopic_array_records.append(record_id)
                subtopics = []
            if primary and primary not in subtopics:
                primary_not_in_links_records.append(record_id)

            for subtopic_id in subtopics:
                pair = (record_id, subtopic_id)
                if pair in seen_record_subtopic_pairs:
                    duplicate_record_subtopic_pairs.append(f"{record_id}::{subtopic_id}")
                seen_record_subtopic_pairs.add(pair)
                if subtopic_id not in catalog_ids:
                    missing_catalog_subtopics.add(subtopic_id)
                if subtopic_id not in curriculum_ids:
                    missing_curriculum_subtopics.add(subtopic_id)

    duplicate_record_ids = [item for item, count in Counter(record_ids).items() if count > 1]

    blocked_records = sorted(
        set(
            invalid_link_status_records
            + missing_retrieval_text_records
            + invalid_visibility_default_records
            + missing_primary_records
            + missing_subtopic_array_records
            + primary_not_in_links_records
            + orphan_record_packet_refs
        )
    )
    blocked_packets = sorted(
        {packet_id for packet_id, count in packet_record_counts.items() if count == 0}
    )

    checks: list[bool] = [
        not duplicate_packet_ids,
        not duplicate_record_ids,
        not invalid_link_status_records,
        not invalid_visibility_default_records,
        not missing_retrieval_text_records,
        not missing_primary_records,
        not missing_subtopic_array_records,
        not primary_not_in_links_records,
        not missing_catalog_subtopics,
        not missing_curriculum_subtopics,
        not duplicate_record_subtopic_pairs,
        not empty_packets,
        not orphan_record_packet_refs,
    ]

    if packet_id is None and isinstance(manifest, dict):
        checks.extend(
            [
                manifest.get("packet_count") == len(packets),
                manifest.get("record_count") == len(records_jsonl or []),
            ]
        )

    status = "pass" if all(checks) else "fail"
    return {
        "status": status,
        "packet_count": len(packets),
        "record_count": len(record_ids),
        "manifest_packet_count": (
            manifest.get("packet_count") if isinstance(manifest, dict) else None
        ),
        "manifest_record_count": (
            manifest.get("record_count") if isinstance(manifest, dict) else None
        ),
        "duplicate_packet_ids": sorted(str(item) for item in duplicate_packet_ids if item),
        "duplicate_record_ids": sorted(duplicate_record_ids),
        "invalid_link_status_records": sorted(invalid_link_status_records),
        "invalid_visibility_default_records": sorted(invalid_visibility_default_records),
        "missing_retrieval_text_records": sorted(missing_retrieval_text_records),
        "missing_primary_records": sorted(missing_primary_records),
        "missing_subtopic_array_records": sorted(missing_subtopic_array_records),
        "primary_not_in_links_records": sorted(primary_not_in_links_records),
        "missing_catalog_subtopics": sorted(missing_catalog_subtopics),
        "missing_curriculum_subtopics": sorted(missing_curriculum_subtopics),
        "duplicate_record_subtopic_pairs": sorted(duplicate_record_subtopic_pairs),
        "empty_packets": sorted(empty_packets),
        "orphan_record_packet_refs": sorted(orphan_record_packet_refs),
        "blocked_packets": blocked_packets,
        "blocked_records": blocked_records,
    }


def build_expected_snapshot(packet_id: str | None = None) -> dict[str, Any]:
    packets = iter_packets(packet_id=packet_id)
    packet_ids = sorted(
        str(found_id) for packet in packets if (found_id := packet.get("packet_id"))
    )
    record_ids: list[str] = []
    record_subtopic_pairs: set[tuple[str, str]] = set()

    for packet in packets:
        for record in packet.get("records") or []:
            record_id = record.get("record_id")
            if not isinstance(record_id, str):
                continue
            record_ids.append(record_id)
            for subtopic_id in record.get("subtopic_ids") or []:
                if isinstance(subtopic_id, str) and subtopic_id:
                    record_subtopic_pairs.add((record_id, subtopic_id))

    return {
        "packet_ids": packet_ids,
        "record_ids": sorted(record_ids),
        "record_subtopic_pairs": sorted(record_subtopic_pairs),
        "packet_count": len(packet_ids),
        "record_count": len(record_ids),
        "link_count": len(record_subtopic_pairs),
    }
