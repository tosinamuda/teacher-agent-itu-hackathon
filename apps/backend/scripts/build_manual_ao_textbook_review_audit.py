"""Build structured review-audit shards for manual AO-textbook linkage rows.

This script does not decide semantic linkage. It only projects already-authored
manual row JSON into smaller review artifacts:

- one file per curriculum subtopic
- one file per atomic objective
- one file per textbook chapter
- one manifest and one Markdown index

Usage:
    uv run python scripts/build_manual_ao_textbook_review_audit.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any, cast

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

DEFAULT_ATOMIC_OBJECTIVES_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "processed"
    / "curriculum"
    / "manual_authoring"
    / "jss1-math_atomic_objectives_all_topics.jsonl"
)
DEFAULT_LINKAGE_DIR = PROJECT_ROOT / "dataset" / "processed" / "ao_textbook_linkage" / "manual"
DEFAULT_OUTPUT_DIR = DEFAULT_LINKAGE_DIR / "review_audit"

JsonObject = dict[str, Any]


def main() -> int:
    from scripts.textbook_corpus_lib import linked_records_path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--linkage-dir",
        default=str(DEFAULT_LINKAGE_DIR),
        help="Directory containing manual linkage row JSON files and manifest.json.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory to write structured review-audit shards.",
    )
    parser.add_argument(
        "--atomic-objectives",
        default=str(DEFAULT_ATOMIC_OBJECTIVES_PATH),
        help="Path to the atomic-objective JSONL source.",
    )
    parser.add_argument(
        "--records",
        default=str(linked_records_path()),
        help="Path to linked textbook records JSONL.",
    )
    parser.add_argument(
        "--generated-at",
        default=date.today().isoformat(),
        help="Date stamp to embed in the generated structured audit manifest.",
    )
    args = parser.parse_args()

    manifest = build_structured_review_audit(
        linkage_dir=Path(args.linkage_dir),
        output_dir=Path(args.output_dir),
        atomic_objectives_path=Path(args.atomic_objectives),
        records_path=Path(args.records),
        generated_at=str(args.generated_at),
    )
    print(
        json.dumps(
            {
                "output_dir": str(Path(args.output_dir)),
                "row_count": manifest["row_count"],
                "subtopic_file_count": manifest["subtopic_file_count"],
                "atomic_objective_file_count": manifest["atomic_objective_file_count"],
                "chapter_file_count": manifest["chapter_file_count"],
                "candidate_atomic_objective_count": manifest["candidate_atomic_objective_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_structured_review_audit(
    *,
    linkage_dir: Path,
    output_dir: Path,
    atomic_objectives_path: Path,
    records_path: Path,
    generated_at: str,
) -> JsonObject:
    from app.domains.expert_content.application.linkage_inference import (
        flatten_atomic_objectives,
        load_reduced_subtopic_textbook_records,
        load_subtopic_atomic_objective_source,
    )
    from app.domains.expert_content.application.linkage_models import (
        ManualSubtopicLinkageRow,
    )
    from app.domains.expert_content.application.linkage_validation import (
        validate_manual_linkage_row,
    )

    linkage_manifest = _load_json(linkage_dir / "manifest.json")
    manifest_rows = _manifest_rows(linkage_manifest)

    output_dir.mkdir(parents=True, exist_ok=True)
    subtopic_dir = output_dir / "subtopics"
    atomic_objective_dir = output_dir / "atomic_objectives"
    chapter_dir = output_dir / "chapters"
    subtopic_dir.mkdir(parents=True, exist_ok=True)
    atomic_objective_dir.mkdir(parents=True, exist_ok=True)
    chapter_dir.mkdir(parents=True, exist_ok=True)

    subtopic_manifest_entries: list[JsonObject] = []
    atomic_objective_manifest_entries: list[JsonObject] = []
    chapter_entries: dict[str, list[JsonObject]] = defaultdict(list)
    status_counts: Counter[str] = Counter()
    candidate_review_counts: Counter[str] = Counter()
    candidate_kind_counts: Counter[str] = Counter()
    candidate_count = 0
    candidate_source_record_count = 0
    record_subtopic_link_count = 0
    needs_review_count = 0
    needs_review_candidate_review_count = 0

    for manifest_row in manifest_rows:
        subtopic_id = str(manifest_row["subtopic_id"])
        row_path = PROJECT_ROOT / str(manifest_row["path"])
        row_payload = _load_json(row_path)
        row = ManualSubtopicLinkageRow.model_validate(row_payload)
        status_counts[row.status] += 1
        if row.status == "needs_review":
            needs_review_count += 1
            if row.candidate_atomic_objective_review is not None:
                needs_review_candidate_review_count += 1

        atomic_source = load_subtopic_atomic_objective_source(
            atomic_objectives_path,
            subtopic_id,
        )
        source_atomic_objectives = flatten_atomic_objectives(atomic_source)
        textbook_records = load_reduced_subtopic_textbook_records(records_path, subtopic_id)
        validation_report = validate_manual_linkage_row(
            row_payload=row_payload,
            atomic_objective_source=atomic_source,
            textbook_records=textbook_records,
        )
        if not validation_report.valid:
            raise ValueError(
                f"Cannot build structured audit for invalid row {subtopic_id}: "
                f"{validation_report.errors}"
            )

        record_subtopic_link_count += len(textbook_records)
        record_map = {str(record.get("record_id") or ""): record for record in textbook_records}
        placement_by_record_id = _placements_by_record_id(row)
        candidate_by_ao_id = _candidates_by_closest_ao(row)
        candidate_count += len(row.candidate_atomic_objectives)
        for candidate in row.candidate_atomic_objectives:
            candidate_kind_counts[candidate.candidate_kind] += 1
            candidate_source_record_count += len(candidate.source_record_ids)

        if row.candidate_atomic_objective_review is not None:
            candidate_review_counts[row.candidate_atomic_objective_review.verdict] += 1

        subtopic_payload = _build_subtopic_payload(
            row=row,
            atomic_source=atomic_source,
            source_atomic_objectives=source_atomic_objectives,
            textbook_records=textbook_records,
            placement_by_record_id=placement_by_record_id,
            candidate_by_ao_id=candidate_by_ao_id,
        )
        subtopic_path = subtopic_dir / f"{subtopic_id}.json"
        _write_json(subtopic_path, subtopic_payload)

        subtopic_chapters = sorted(
            {
                _chapter_slug_from_record(record)
                for record in textbook_records
                if _chapter_slug_from_record(record)
            }
        )
        subtopic_manifest_entries.append(
            {
                "subtopic_id": row.subtopic_id,
                "subtopic_title": row.subtopic_title,
                "status": row.status,
                "path": _relative(subtopic_path),
                "source_record_count": len(textbook_records),
                "atomic_objective_count": len(row.atomic_objectives),
                "candidate_atomic_objective_count": len(row.candidate_atomic_objectives),
                "candidate_review_verdict": (
                    row.candidate_atomic_objective_review.verdict
                    if row.candidate_atomic_objective_review is not None
                    else None
                ),
                "textbook_chapters": subtopic_chapters,
            }
        )

        for atomic_objective in row.atomic_objectives:
            ao_payload = _build_atomic_objective_payload(
                row=row,
                atomic_objective=atomic_objective,
                record_map=record_map,
                candidate_atomic_objectives=candidate_by_ao_id[atomic_objective.ao_id],
            )
            ao_path = atomic_objective_dir / f"{atomic_objective.ao_id}.json"
            _write_json(ao_path, ao_payload)
            atomic_objective_manifest_entries.append(
                {
                    "ao_id": atomic_objective.ao_id,
                    "subtopic_id": row.subtopic_id,
                    "path": _relative(ao_path),
                    "evidence_classification": atomic_objective.evidence_classification,
                    "record_link_count": len(atomic_objective.record_links),
                    "candidate_atomic_objective_count": len(
                        candidate_by_ao_id[atomic_objective.ao_id]
                    ),
                }
            )

        for record in textbook_records:
            record_id = str(record.get("record_id") or "")
            chapter_slug = _chapter_slug_from_record(record)
            chapter_entries[chapter_slug].append(
                {
                    "subtopic_id": row.subtopic_id,
                    "subtopic_title": row.subtopic_title,
                    "record": _record_view(
                        record,
                        placement_by_record_id.get(record_id, {"bucket": "unaccounted"}),
                        include_full_text=False,
                    ),
                }
            )

    chapter_manifest_entries: list[JsonObject] = []
    for chapter_slug, entries in sorted(chapter_entries.items()):
        chapter_payload = {
            "schema_version": "manual-ao-textbook-review-audit-chapter-v1",
            "chapter_slug": chapter_slug,
            "chapter_title": entries[0]["record"]["chapter_title"],
            "record_subtopic_link_count": len(entries),
            "subtopic_count": len({entry["subtopic_id"] for entry in entries}),
            "entries": entries,
        }
        chapter_path = chapter_dir / f"{chapter_slug}.json"
        _write_json(chapter_path, chapter_payload)
        chapter_manifest_entries.append(
            {
                "chapter_slug": chapter_slug,
                "chapter_title": chapter_payload["chapter_title"],
                "path": _relative(chapter_path),
                "record_subtopic_link_count": len(entries),
                "subtopic_count": chapter_payload["subtopic_count"],
            }
        )

    structured_manifest = {
        "schema_version": "manual-ao-textbook-review-audit-v1",
        "generated_at": generated_at,
        "source_linkage_manifest_path": _relative(linkage_dir / "manifest.json"),
        "atomic_objectives_path": _relative(atomic_objectives_path),
        "textbook_records_path": _relative(records_path),
        "row_count": len(manifest_rows),
        "status_counts": dict(sorted(status_counts.items())),
        "needs_review_count": needs_review_count,
        "needs_review_candidate_review_count": needs_review_candidate_review_count,
        "subtopic_file_count": len(subtopic_manifest_entries),
        "atomic_objective_file_count": len(atomic_objective_manifest_entries),
        "chapter_file_count": len(chapter_manifest_entries),
        "record_subtopic_link_count": record_subtopic_link_count,
        "candidate_atomic_objective_count": candidate_count,
        "candidate_atomic_objective_kind_counts": dict(sorted(candidate_kind_counts.items())),
        "candidate_source_record_count": candidate_source_record_count,
        "candidate_review_verdict_counts": dict(sorted(candidate_review_counts.items())),
        "subtopics": subtopic_manifest_entries,
        "atomic_objectives": atomic_objective_manifest_entries,
        "chapters": chapter_manifest_entries,
    }
    _write_json(output_dir / "manifest.json", structured_manifest)
    _write_index(output_dir / "INDEX.md", structured_manifest)
    return structured_manifest


def _build_subtopic_payload(
    *,
    row: Any,
    atomic_source: JsonObject,
    source_atomic_objectives: list[JsonObject],
    textbook_records: list[JsonObject],
    placement_by_record_id: dict[str, JsonObject],
    candidate_by_ao_id: dict[str, list[JsonObject]],
) -> JsonObject:
    return {
        "schema_version": "manual-ao-textbook-review-audit-subtopic-v1",
        "subtopic_id": row.subtopic_id,
        "subtopic_title": row.subtopic_title,
        "topic": atomic_source.get("topic"),
        "topic_key": atomic_source.get("topic_key"),
        "theme_key": atomic_source.get("theme_key"),
        "status": row.status,
        "status_reasons": list(row.status_reasons),
        "review_categories": list(row.review_categories),
        "category_reasons": [item.model_dump(mode="json") for item in row.category_reasons],
        "candidate_atomic_objective_review": (
            row.candidate_atomic_objective_review.model_dump(mode="json")
            if row.candidate_atomic_objective_review is not None
            else None
        ),
        "candidate_atomic_objectives": [
            item.model_dump(mode="json") for item in row.candidate_atomic_objectives
        ],
        "curriculum_objectives": atomic_source.get("curriculum_objectives") or [],
        "atomic_objectives": [
            _atomic_objective_summary(ao, candidate_by_ao_id[ao.ao_id])
            for ao in row.atomic_objectives
        ],
        "source_atomic_objective_order": [item["ao_id"] for item in source_atomic_objectives],
        "record_accounting": _record_accounting(row),
        "records": [
            _record_view(
                record,
                placement_by_record_id.get(
                    str(record.get("record_id") or ""),
                    {"bucket": "unaccounted"},
                ),
                include_full_text=True,
            )
            for record in textbook_records
        ],
    }


def _build_atomic_objective_payload(
    *,
    row: Any,
    atomic_objective: Any,
    record_map: dict[str, JsonObject],
    candidate_atomic_objectives: list[JsonObject],
) -> JsonObject:
    record_links = []
    for link in atomic_objective.record_links:
        record = record_map[link.record_id]
        record_links.append(
            {
                **link.model_dump(mode="json"),
                "record": _record_view(
                    record,
                    {"bucket": "ao_record_link", "ao_id": atomic_objective.ao_id},
                    include_full_text=True,
                ),
            }
        )

    return {
        "schema_version": "manual-ao-textbook-review-audit-ao-v1",
        "subtopic_id": row.subtopic_id,
        "subtopic_title": row.subtopic_title,
        "row_status": row.status,
        "ao_id": atomic_objective.ao_id,
        "ao_order": atomic_objective.ao_order,
        "curriculum_objective_id": atomic_objective.curriculum_objective_id,
        "curriculum_objective_text": atomic_objective.curriculum_objective_text,
        "text": atomic_objective.text,
        "bloom_verb": atomic_objective.bloom_verb,
        "bloom_level": atomic_objective.bloom_level,
        "evidence_classification": atomic_objective.evidence_classification,
        "review_categories": list(atomic_objective.review_categories),
        "record_links": record_links,
        "practice_record_ids": list(atomic_objective.practice_record_ids),
        "step_blueprint": atomic_objective.step_blueprint.model_dump(mode="json"),
        "assessment": (
            atomic_objective.assessment.model_dump(mode="json")
            if atomic_objective.assessment is not None
            else None
        ),
        "closest_candidate_atomic_objectives": candidate_atomic_objectives,
    }


def _atomic_objective_summary(
    atomic_objective: Any,
    candidate_atomic_objectives: list[JsonObject],
) -> JsonObject:
    return {
        "ao_id": atomic_objective.ao_id,
        "ao_order": atomic_objective.ao_order,
        "curriculum_objective_id": atomic_objective.curriculum_objective_id,
        "text": atomic_objective.text,
        "bloom_verb": atomic_objective.bloom_verb,
        "bloom_level": atomic_objective.bloom_level,
        "evidence_classification": atomic_objective.evidence_classification,
        "review_categories": list(atomic_objective.review_categories),
        "record_link_ids": [link.record_id for link in atomic_objective.record_links],
        "practice_record_ids": list(atomic_objective.practice_record_ids),
        "has_assessment": atomic_objective.assessment is not None,
        "closest_candidate_atomic_objective_ids": [
            item["candidate_ao_id"] for item in candidate_atomic_objectives
        ],
    }


def _placements_by_record_id(row: Any) -> dict[str, JsonObject]:
    placements: dict[str, JsonObject] = {}
    for record_id in row.shared_foundation_record_ids:
        placements[record_id] = {"bucket": "shared_foundation"}
    for item in row.excluded_records:
        placements[item.record_id] = {
            "bucket": "excluded",
            "record_type": item.record_type,
            "reason": item.reason,
        }
    for item in row.review_items:
        placements[item.record_id] = {
            "bucket": "review_item",
            "candidate_ao_ids": list(item.candidate_ao_ids),
            "candidate_roles": list(item.candidate_roles),
            "issue": item.issue,
            "rationale": item.rationale,
        }
    for atomic_objective in row.atomic_objectives:
        for link in atomic_objective.record_links:
            placements[link.record_id] = {
                "bucket": "ao_record_link",
                "ao_id": atomic_objective.ao_id,
                "role": link.role,
                "method": link.method,
                "rationale": link.rationale,
            }
    return placements


def _candidates_by_closest_ao(row: Any) -> dict[str, list[JsonObject]]:
    grouped: dict[str, list[JsonObject]] = defaultdict(list)
    for atomic_objective in row.atomic_objectives:
        grouped[atomic_objective.ao_id] = []
    for candidate in row.candidate_atomic_objectives:
        payload = candidate.model_dump(mode="json")
        for ao_id in candidate.closest_existing_ao_ids:
            grouped[ao_id].append(payload)
    return grouped


def _record_accounting(row: Any) -> JsonObject:
    return {
        "shared_foundation_record_ids": list(row.shared_foundation_record_ids),
        "excluded_record_ids": [item.record_id for item in row.excluded_records],
        "review_record_ids": [item.record_id for item in row.review_items],
        "ao_record_link_ids": [
            link.record_id
            for atomic_objective in row.atomic_objectives
            for link in atomic_objective.record_links
        ],
    }


def _record_view(
    record: JsonObject,
    placement: JsonObject,
    *,
    include_full_text: bool,
) -> JsonObject:
    heading_path = _normalise_heading_path(record.get("heading_path"))
    payload: JsonObject = {
        "record_id": str(record.get("record_id") or ""),
        "record_type": str(record.get("record_type") or ""),
        "chapter_title": heading_path["h1"] or "unknown-chapter",
        "chapter_slug": _chapter_slug_from_heading(heading_path),
        "heading_path": heading_path,
        "primary_subtopic_id": record.get("primary_subtopic_id"),
        "placement": placement,
        "evidence_quote": _evidence_quote(record),
    }
    if include_full_text:
        payload.update(
            {
                "content_text": str(record.get("content_text") or ""),
                "prompt_text": str(record.get("prompt_text") or ""),
                "answer_text": str(record.get("answer_text") or ""),
            }
        )
    return payload


def _normalise_heading_path(value: Any) -> JsonObject:
    if isinstance(value, dict):
        return {
            "h1": value.get("h1"),
            "h2": value.get("h2"),
            "h3": value.get("h3"),
        }
    if isinstance(value, list):
        items = [str(item) for item in value]
        return {
            "h1": items[0] if len(items) > 0 else None,
            "h2": items[1] if len(items) > 1 else None,
            "h3": items[2] if len(items) > 2 else None,
        }
    if isinstance(value, str):
        items = [item.strip() for item in value.split(">")]
        return {
            "h1": items[0] if len(items) > 0 else None,
            "h2": items[1] if len(items) > 1 else None,
            "h3": items[2] if len(items) > 2 else None,
        }
    return {"h1": None, "h2": None, "h3": None}


def _chapter_slug_from_record(record: JsonObject) -> str:
    return _chapter_slug_from_heading(_normalise_heading_path(record.get("heading_path")))


def _chapter_slug_from_heading(heading_path: JsonObject) -> str:
    title = str(heading_path.get("h1") or "unknown-chapter")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "unknown-chapter"


def _evidence_quote(record: JsonObject) -> str:
    text = (
        str(record.get("content_text") or "")
        or str(record.get("prompt_text") or "")
        or str(record.get("answer_text") or "")
    )
    return re.sub(r"\s+", " ", text).strip()[:320]


def _manifest_rows(manifest: JsonObject) -> list[JsonObject]:
    rows = manifest.get("rows")
    if not isinstance(rows, list):
        raise ValueError("manual linkage manifest rows must be a list")
    return [cast(JsonObject, item) for item in rows if isinstance(item, dict)]


def _load_json(path: Path) -> JsonObject:
    return cast(JsonObject, json.loads(path.read_text(encoding="utf-8")))


def _write_json(path: Path, payload: JsonObject) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_index(path: Path, manifest: JsonObject) -> None:
    lines = [
        "# Manual AO-Textbook Review Audit Index",
        "",
        "This directory is the reviewable audit artifact. Use the JSON shards, not the",
        "monolithic `REVIEW_AUDIT.md`, when checking linkage or candidate-AO decisions.",
        "",
        "## Summary",
        "",
        f"- Rows: {manifest['row_count']}",
        f"- Needs-review rows: {manifest['needs_review_count']}",
        "- Needs-review rows with candidate review verdict: "
        f"{manifest['needs_review_candidate_review_count']}",
        f"- Subtopic files: {manifest['subtopic_file_count']}",
        f"- Atomic-objective files: {manifest['atomic_objective_file_count']}",
        f"- Chapter files: {manifest['chapter_file_count']}",
        f"- Candidate atomic objectives: {manifest['candidate_atomic_objective_count']}",
        f"- Candidate source-record references: {manifest['candidate_source_record_count']}",
        "",
        "## How To Review",
        "",
        "- Start with `manifest.json` for counts and file paths.",
        "- Review one `subtopics/<subtopic_id>.json` file at a time for row-level",
        "  accounting, candidate verdicts, and record placement.",
        "- Review `atomic_objectives/<ao_id>.json` for AO-specific evidence.",
        "- Review `chapters/<chapter>.json` when checking textbook-section reuse across",
        "  multiple subtopics.",
        "",
        "## Candidate Rows",
        "",
    ]
    for entry in manifest["subtopics"]:
        if int(entry["candidate_atomic_objective_count"]) == 0:
            continue
        lines.append(
            "- "
            f"`{entry['subtopic_id']}`: "
            f"{entry['candidate_atomic_objective_count']} candidate(s), "
            f"{entry['path']}"
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
