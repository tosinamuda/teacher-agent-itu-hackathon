from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domains.expert_content.application import (
    REVIEW_CATEGORY_DESCRIPTIONS,
    build_atomic_objective_rollup,
    build_candidate_atomic_objective_rollup,
    build_manual_ao_textbook_linkage_prompt,
    build_manual_linkage_review_triage_report,
    flatten_atomic_objectives,
    infer_bloom_level,
    infer_bloom_verb,
    load_reduced_subtopic_textbook_records,
    load_subtopic_atomic_objective_source,
    validate_manual_linkage_row,
)

REPO_ROOT = Path(__file__).resolve().parents[2].parent
ATOMIC_OBJECTIVES_PATH = (
    REPO_ROOT
    / "dataset"
    / "processed"
    / "curriculum"
    / "manual_authoring"
    / "jss1-math_atomic_objectives_all_topics.jsonl"
)
TEXTBOOK_RECORDS_PATH = (
    REPO_ROOT / "dataset" / "processed" / "textbook" / "jsonl" / "linked" / "records.jsonl"
)
PROMPT_TEMPLATE_PATH = REPO_ROOT / "apps/backend/scripts/manual_ao_textbook_linkage_prompt.md"
MANUAL_LINKAGE_DIR = REPO_ROOT / "dataset" / "processed" / "ao_textbook_linkage" / "manual"
MANIFEST_PATH = MANUAL_LINKAGE_DIR / "manifest.json"
REVIEW_TRIAGE_PATH = MANUAL_LINKAGE_DIR / "review_triage.json"
REVIEW_AUDIT_DIR = MANUAL_LINKAGE_DIR / "review_audit"
REVIEW_AUDIT_MANIFEST_PATH = REVIEW_AUDIT_DIR / "manifest.json"
PILOT_SUBTOPIC_ID = "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
PILOT_ROW_PATH = MANUAL_LINKAGE_DIR / f"{PILOT_SUBTOPIC_ID}.json"


def _all_curriculum_subtopic_ids() -> list[str]:
    ids: list[str] = []
    with ATOMIC_OBJECTIVES_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            ids.append(json.loads(line)["subtopic_id"])
    return ids


def _all_manual_linkage_payloads() -> list[dict[str, object]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    payloads: list[dict[str, object]] = []
    for entry in manifest.get("rows", []):
        row_path = REPO_ROOT / entry["path"]
        payloads.append(json.loads(row_path.read_text(encoding="utf-8")))
    return payloads


def _review_audit_manifest() -> dict[str, object]:
    return json.loads(REVIEW_AUDIT_MANIFEST_PATH.read_text(encoding="utf-8"))


def _review_audit_subtopic_payloads() -> dict[str, dict[str, object]]:
    audit_manifest = _review_audit_manifest()
    payloads: dict[str, dict[str, object]] = {}
    for entry in audit_manifest["subtopics"]:
        path = REPO_ROOT / entry["path"]
        payloads[entry["subtopic_id"]] = json.loads(path.read_text(encoding="utf-8"))
    return payloads


def test_manual_linkage_extracts_pilot_inputs() -> None:
    atomic_source = load_subtopic_atomic_objective_source(
        ATOMIC_OBJECTIVES_PATH,
        PILOT_SUBTOPIC_ID,
    )
    atomic_objectives = flatten_atomic_objectives(atomic_source)
    textbook_records = load_reduced_subtopic_textbook_records(
        TEXTBOOK_RECORDS_PATH,
        PILOT_SUBTOPIC_ID,
    )

    assert atomic_source["subtopic_id"] == PILOT_SUBTOPIC_ID
    assert [item["ao_id"] for item in atomic_objectives] == [
        "fractions-to-decimals-ao-convert-fractions-to-decimals",
        "fractions-to-decimals-ao-convert-decimals-to-fractions",
    ]
    assert len(textbook_records) == 32
    assert textbook_records[0]["record_id"] == "ch01-b013"
    assert textbook_records[-1]["record_id"] == "ch04-b058"


def test_manual_linkage_prompt_uses_reduced_payload_and_corrected_role_name() -> None:
    atomic_source = load_subtopic_atomic_objective_source(
        ATOMIC_OBJECTIVES_PATH,
        PILOT_SUBTOPIC_ID,
    )
    textbook_records = load_reduced_subtopic_textbook_records(
        TEXTBOOK_RECORDS_PATH,
        PILOT_SUBTOPIC_ID,
    )
    prompt = build_manual_ao_textbook_linkage_prompt(
        template_text=PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8"),
        atomic_objective_source=atomic_source,
        textbook_records=textbook_records[:1],
    )

    assert "{{ATOMIC_OBJECTIVES}}" not in prompt
    assert "{{TEXTBOOK_RECORDS}}" not in prompt
    assert '"record_id": "ch01-b013"' in prompt
    assert '"raw_html"' not in prompt
    assert "worked_example" in prompt
    assert "modeling" not in prompt


def test_manual_linkage_validator_accepts_checked_in_pilot_row() -> None:
    atomic_source = load_subtopic_atomic_objective_source(
        ATOMIC_OBJECTIVES_PATH,
        PILOT_SUBTOPIC_ID,
    )
    textbook_records = load_reduced_subtopic_textbook_records(
        TEXTBOOK_RECORDS_PATH,
        PILOT_SUBTOPIC_ID,
    )
    pilot_row = json.loads(PILOT_ROW_PATH.read_text(encoding="utf-8"))

    report = validate_manual_linkage_row(
        row_payload=pilot_row,
        atomic_objective_source=atomic_source,
        textbook_records=textbook_records,
    )

    assert report.valid is True
    assert report.errors == []
    assert report.total_source_records == 32
    assert report.shared_foundation_count == 12
    assert report.excluded_record_count == 6
    assert report.review_record_count == 0


def test_every_curriculum_subtopic_has_a_linkage_row() -> None:
    expected_ids = _all_curriculum_subtopic_ids()
    missing: list[str] = []
    for subtopic_id in expected_ids:
        row_path = MANUAL_LINKAGE_DIR / f"{subtopic_id}.json"
        if not row_path.is_file():
            missing.append(subtopic_id)
    assert not missing, (
        f"Missing manual AO-textbook linkage rows for {len(missing)} subtopic(s): "
        f"{missing[:5]}{'…' if len(missing) > 5 else ''}"
    )


def test_manifest_lists_every_curriculum_subtopic_row() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_ids = _all_curriculum_subtopic_ids()
    manifest_ids = [entry["subtopic_id"] for entry in manifest.get("rows", [])]
    assert manifest["row_count"] == len(expected_ids)
    assert sorted(manifest_ids) == sorted(expected_ids)


def test_manual_linkage_review_triage_report_matches_current_rows() -> None:
    report = json.loads(REVIEW_TRIAGE_PATH.read_text(encoding="utf-8"))
    expected = build_manual_linkage_review_triage_report(
        _all_manual_linkage_payloads(),
        generated_at=report["generated_at"],
    )

    assert report["schema_version"] == "manual-ao-textbook-linkage-review-triage-v2"
    assert report["row_count"] == expected["row_count"]
    assert report["status_counts"] == expected["status_counts"]
    assert report["category_counts"] == expected["category_counts"]
    assert (
        report["candidate_atomic_objective_rollup"] == expected["candidate_atomic_objective_rollup"]
    )
    assert report["rows"] == expected["rows"]


def test_structured_review_audit_covers_every_subtopic_with_evidence_quotes() -> None:
    """The structured review audit must exist and cover every subtopic.

    The audit shards are the persistent inspection trail showing the AO and
    textbook record content that grounds each manually authored category. The
    test only checks structural presence; it never invents categories.
    """
    audit_manifest = _review_audit_manifest()
    expected_ids = _all_curriculum_subtopic_ids()
    audit_ids = [entry["subtopic_id"] for entry in audit_manifest["subtopics"]]

    assert audit_manifest["schema_version"] == "manual-ao-textbook-review-audit-v1"
    assert audit_manifest["row_count"] == len(expected_ids)
    assert audit_manifest["subtopic_file_count"] == len(expected_ids)
    assert sorted(audit_ids) == sorted(expected_ids)

    for entry in audit_manifest["subtopics"]:
        path = REPO_ROOT / entry["path"]
        assert path.is_file(), f"Audit shard is missing for {entry['subtopic_id']}"


def test_structured_review_audit_has_one_evidence_quote_per_record_subtopic_link() -> None:
    """Every record-subtopic link must be cited with an evidence quote in the
    structured audit. The expected total is the sum of `source_record_count`
    across all manifest rows.
    """
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_quote_count = sum(entry["source_record_count"] for entry in manifest["rows"])
    audit_manifest = _review_audit_manifest()
    subtopic_payloads = _review_audit_subtopic_payloads()
    actual_quote_count = sum(len(payload["records"]) for payload in subtopic_payloads.values())

    assert audit_manifest["record_subtopic_link_count"] == expected_quote_count
    assert actual_quote_count == expected_quote_count, (
        f"Structured review audit has {actual_quote_count} evidence quotes but the "
        f"row payloads account for {expected_quote_count} record-subtopic "
        f"links (sum of source_record_count across all rows)."
    )
    for payload in subtopic_payloads.values():
        for record in payload["records"]:
            assert record["evidence_quote"].strip(), (
                f"Audit record {record['record_id']} in {payload['subtopic_id']} "
                "is missing an evidence quote"
            )


def test_ao_rollup_matches_row_payloads() -> None:
    """The triage report's AO rollup must equal the rollup derived from row
    payloads, and the per-row AO totals must add up to the cumulative AO count
    in the curriculum source.
    """
    report = json.loads(REVIEW_TRIAGE_PATH.read_text(encoding="utf-8"))
    payloads = _all_manual_linkage_payloads()
    expected = build_atomic_objective_rollup(payloads)
    assert report["atomic_objective_rollup"] == expected

    # The AO total derived from row payloads must equal the AO total derived
    # from the curriculum source. This guards against an AO being dropped or
    # duplicated in the row JSONs.
    curriculum_ao_count = 0
    for subtopic_id in _all_curriculum_subtopic_ids():
        atomic_source = load_subtopic_atomic_objective_source(ATOMIC_OBJECTIVES_PATH, subtopic_id)
        curriculum_ao_count += len(flatten_atomic_objectives(atomic_source))
    assert expected["total_atomic_objectives"] == curriculum_ao_count

    # The classifications and counts must partition every AO.
    ev_total = sum(expected["evidence_classification_counts"].values())
    assert ev_total == expected["total_atomic_objectives"], (
        "evidence_classification must be set on every AO"
    )

    # AOs flagged with no_reused_assessment must each have assessment=null.
    review_no_reused = expected["review_category_counts"].get("no_reused_assessment", 0)
    assert review_no_reused <= expected["atomic_objectives_without_assessment"]


def test_candidate_ao_rollup_matches_row_payloads() -> None:
    report = json.loads(REVIEW_TRIAGE_PATH.read_text(encoding="utf-8"))
    payloads = _all_manual_linkage_payloads()
    expected = build_candidate_atomic_objective_rollup(payloads)

    assert report["candidate_atomic_objective_rollup"] == expected
    assert expected["total_candidate_atomic_objectives"] > 0
    assert expected["candidate_source_record_count"] > 0
    assert expected["candidate_status_counts"] == {
        "candidate_for_expert_review": expected["total_candidate_atomic_objectives"]
    }


def test_candidate_ao_references_are_valid_and_auditable() -> None:
    payloads = _all_manual_linkage_payloads()
    subtopic_audits = _review_audit_subtopic_payloads()
    all_candidate_ids: list[str] = []

    for row in payloads:
        candidates = row.get("candidate_atomic_objectives") or []
        candidate_review = row.get("candidate_atomic_objective_review")
        categories = set(row.get("review_categories") or [])
        category_reasons = {
            item["category"]: item["reason"] for item in row.get("category_reasons") or []
        }
        row_ao_ids = {item["ao_id"] for item in row.get("atomic_objectives") or []}
        excluded_ids = {item["record_id"] for item in row.get("excluded_records") or []}
        source_records = load_reduced_subtopic_textbook_records(
            TEXTBOOK_RECORDS_PATH,
            str(row["subtopic_id"]),
        )
        source_record_ids = {str(record["record_id"]) for record in source_records}

        if "candidate_new_atomic_objective" in categories:
            assert candidates, (
                f"{row['subtopic_id']} has candidate_new_atomic_objective "
                "without candidate proposals"
            )
            assert candidate_review["verdict"] == "has_candidates"
            assert category_reasons["candidate_new_atomic_objective"]
        elif candidate_review is not None:
            assert candidate_review["verdict"] != "has_candidates"

        audit_candidates = {
            item["candidate_ao_id"]: item
            for item in subtopic_audits[str(row["subtopic_id"])]["candidate_atomic_objectives"]
        }
        for candidate in candidates:
            all_candidate_ids.append(candidate["candidate_ao_id"])
            assert candidate["status"] == "candidate_for_expert_review"
            assert candidate["source_record_ids"]
            assert set(candidate["source_record_ids"]) <= source_record_ids
            assert not (set(candidate["source_record_ids"]) & excluded_ids)
            assert set(candidate["closest_existing_ao_ids"]) <= row_ao_ids
            assert candidate["rationale"].strip()
            assert candidate["evidence_quote"].strip()
            assert candidate["bloom_verb"] == infer_bloom_verb(candidate["proposed_objective_text"])
            assert candidate["bloom_level"] == infer_bloom_level(
                candidate["proposed_objective_text"]
            )
            assert candidate["candidate_ao_id"] in audit_candidates
            audit_candidate = audit_candidates[candidate["candidate_ao_id"]]
            assert audit_candidate["evidence_quote"] == candidate["evidence_quote"]
            assert audit_candidate["rationale"] == candidate["rationale"]

    assert all_candidate_ids
    assert len(all_candidate_ids) == len(set(all_candidate_ids))


def test_every_needs_review_row_has_candidate_ao_review_verdict() -> None:
    report = json.loads(REVIEW_TRIAGE_PATH.read_text(encoding="utf-8"))
    needs_review_rows = [row for row in report["rows"] if row["status"] == "needs_review"]

    assert len(needs_review_rows) == report["status_counts"]["needs_review"]
    for row in needs_review_rows:
        review = row["candidate_atomic_objective_review"]
        assert review["reviewed"] is True
        assert review["verdict"] in {"has_candidates", "no_candidate_records"}
        assert review["rationale"].strip()


def test_needs_review_rows_have_actionable_triage_categories() -> None:
    report = json.loads(REVIEW_TRIAGE_PATH.read_text(encoding="utf-8"))
    category_names = set(REVIEW_CATEGORY_DESCRIPTIONS)
    rows = report["rows"]
    needs_review_rows = [row for row in rows if row["status"] == "needs_review"]

    assert needs_review_rows
    assert set(report["category_descriptions"]) == category_names
    assert report["category_counts"]["prerequisite_only_evidence"] > 0

    for row in needs_review_rows:
        categories = set(row["categories"])
        assert categories
        assert categories <= category_names
        assert row["category_reasons"]

    for row in rows:
        if row["status"] == "mapped":
            assert row["categories"] == []
        if row["status"] == "no_records":
            assert "corpus_gap" in row["categories"]


@pytest.mark.parametrize("subtopic_id", _all_curriculum_subtopic_ids())
def test_every_manual_linkage_row_validates(subtopic_id: str) -> None:
    row_path = MANUAL_LINKAGE_DIR / f"{subtopic_id}.json"
    row_payload = json.loads(row_path.read_text(encoding="utf-8"))
    atomic_source = load_subtopic_atomic_objective_source(
        ATOMIC_OBJECTIVES_PATH,
        subtopic_id,
    )
    textbook_records = load_reduced_subtopic_textbook_records(
        TEXTBOOK_RECORDS_PATH,
        subtopic_id,
    )
    report = validate_manual_linkage_row(
        row_payload=row_payload,
        atomic_objective_source=atomic_source,
        textbook_records=textbook_records,
    )
    assert report.valid, f"Manual linkage row failed validation for {subtopic_id}: {report.errors}"


def test_manual_linkage_validator_rejects_missing_record_accounting() -> None:
    atomic_source = load_subtopic_atomic_objective_source(
        ATOMIC_OBJECTIVES_PATH,
        PILOT_SUBTOPIC_ID,
    )
    textbook_records = load_reduced_subtopic_textbook_records(
        TEXTBOOK_RECORDS_PATH,
        PILOT_SUBTOPIC_ID,
    )
    pilot_row = json.loads(PILOT_ROW_PATH.read_text(encoding="utf-8"))
    pilot_row["excluded_records"] = pilot_row["excluded_records"][1:]

    report = validate_manual_linkage_row(
        row_payload=pilot_row,
        atomic_objective_source=atomic_source,
        textbook_records=textbook_records,
    )

    assert report.valid is False
    assert any("source records not accounted for" in error for error in report.errors)


def test_manual_linkage_validator_rejects_candidate_category_without_candidate() -> None:
    atomic_source = load_subtopic_atomic_objective_source(
        ATOMIC_OBJECTIVES_PATH,
        PILOT_SUBTOPIC_ID,
    )
    textbook_records = load_reduced_subtopic_textbook_records(
        TEXTBOOK_RECORDS_PATH,
        PILOT_SUBTOPIC_ID,
    )
    pilot_row = json.loads(PILOT_ROW_PATH.read_text(encoding="utf-8"))
    pilot_row["review_categories"] = ["candidate_new_atomic_objective"]
    pilot_row["category_reasons"] = [
        {
            "category": "candidate_new_atomic_objective",
            "reason": "Synthetic invalid row for validator coverage.",
        }
    ]
    pilot_row["candidate_atomic_objectives"] = []

    report = validate_manual_linkage_row(
        row_payload=pilot_row,
        atomic_objective_source=atomic_source,
        textbook_records=textbook_records,
    )

    assert report.valid is False
    assert any(
        "candidate_new_atomic_objective requires at least one" in error for error in report.errors
    )


def test_manual_linkage_validator_rejects_invalid_candidate_record_references() -> None:
    atomic_source = load_subtopic_atomic_objective_source(
        ATOMIC_OBJECTIVES_PATH,
        PILOT_SUBTOPIC_ID,
    )
    textbook_records = load_reduced_subtopic_textbook_records(
        TEXTBOOK_RECORDS_PATH,
        PILOT_SUBTOPIC_ID,
    )
    pilot_row = json.loads(PILOT_ROW_PATH.read_text(encoding="utf-8"))
    candidate = {
        "candidate_ao_id": "synthetic-candidate-ao",
        "candidate_kind": "missing_direct_objective",
        "proposed_objective_text": "Identify an invalid candidate objective.",
        "bloom_verb": "identify",
        "bloom_level": "remember",
        "source_record_ids": ["unknown-record"],
        "evidence_quote": "Synthetic evidence quote.",
        "closest_existing_ao_ids": [
            pilot_row["atomic_objectives"][0]["ao_id"],
        ],
        "rationale": "Synthetic invalid row for validator coverage.",
        "status": "candidate_for_expert_review",
    }
    pilot_row["candidate_atomic_objectives"] = [candidate]
    pilot_row["review_categories"] = ["candidate_new_atomic_objective"]
    pilot_row["category_reasons"] = [
        {
            "category": "candidate_new_atomic_objective",
            "reason": "Synthetic invalid row for validator coverage.",
        }
    ]

    unknown_report = validate_manual_linkage_row(
        row_payload=pilot_row,
        atomic_objective_source=atomic_source,
        textbook_records=textbook_records,
    )
    assert unknown_report.valid is False
    assert any("contains unknown source_record_ids" in error for error in unknown_report.errors)

    excluded_record_id = pilot_row["excluded_records"][0]["record_id"]
    pilot_row["candidate_atomic_objectives"][0]["source_record_ids"] = [
        excluded_record_id,
    ]
    excluded_report = validate_manual_linkage_row(
        row_payload=pilot_row,
        atomic_objective_source=atomic_source,
        textbook_records=textbook_records,
    )
    assert excluded_report.valid is False
    assert any("references excluded record ids" in error for error in excluded_report.errors)
