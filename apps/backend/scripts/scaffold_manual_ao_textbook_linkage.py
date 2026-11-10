"""Generate a structural scaffold for one subtopic's manual AO-textbook linkage row.

Manual judgment requirement: this script ONLY pre-populates deterministic structural
fields (subtopic_id, subtopic_title, AO order, AO ids, AO text, curriculum-objective
metadata, bloom_verb / bloom_level inferred by the application module) and emits
rule-based exclusions for exercise_block / summary / hint records. It does NOT decide
which records are shared foundation, which AO each record supports, or which records
go to review_items. Those decisions are filled in manually after the scaffold is
emitted.

Usage:
    uv run python scripts/scaffold_manual_ao_textbook_linkage.py \
        --subtopic-id <id> > /tmp/<id>.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


def main() -> int:
    from app.domains.expert_content.application.linkage_inference import (
        flatten_atomic_objectives,
        load_reduced_subtopic_textbook_records,
        load_subtopic_atomic_objective_source,
    )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subtopic-id", required=True)
    parser.add_argument(
        "--atomic-objectives",
        default=str(
            PROJECT_ROOT
            / "dataset"
            / "processed"
            / "curriculum"
            / "manual_authoring"
            / "jss1-math_atomic_objectives_all_topics.jsonl"
        ),
    )
    parser.add_argument(
        "--records",
        default=str(
            PROJECT_ROOT
            / "dataset"
            / "processed"
            / "textbook"
            / "jsonl"
            / "linked"
            / "records.jsonl"
        ),
    )
    args = parser.parse_args()

    src = load_subtopic_atomic_objective_source(Path(args.atomic_objectives), args.subtopic_id)
    aos = flatten_atomic_objectives(src)
    recs = load_reduced_subtopic_textbook_records(Path(args.records), args.subtopic_id)

    rule_excluded_types = {"exercise_block", "summary", "hint"}
    excluded = [
        {
            "record_id": r["record_id"],
            "record_type": r["record_type"],
            "reason": _exclude_reason(r["record_type"]),
        }
        for r in recs
        if r["record_type"] in rule_excluded_types
    ]

    scaffold = {
        "subtopic_id": src["subtopic_id"],
        "subtopic_title": src["subtopic_title"],
        "status": "no_records" if not recs else "needs_review",
        "status_reasons": (
            ["No textbook records are linked to this subtopic in the linked corpus."]
            if not recs
            else []
        ),
        "shared_foundation_record_ids": [],
        "excluded_records": excluded,
        "review_items": [],
        "candidate_atomic_objectives": [],
        "atomic_objectives": [
            {
                "ao_id": ao["ao_id"],
                "ao_order": ao["ao_order"],
                "curriculum_objective_id": ao["curriculum_objective_id"],
                "curriculum_objective_text": ao["curriculum_objective_text"],
                "text": ao["text"],
                "bloom_verb": ao["bloom_verb"],
                "bloom_level": ao["bloom_level"],
                "record_links": [],
                "practice_record_ids": [],
                "step_blueprint": {
                    "block_types": ["explanation"],
                    "instructional_type": "explain_only",
                },
                "assessment": None,
            }
            for ao in aos
        ],
    }

    print(json.dumps(scaffold, ensure_ascii=False, indent=2))
    return 0


def _exclude_reason(record_type: str) -> str:
    if record_type == "exercise_block":
        return "Exercise blocks are excluded; child exercise_items are handled individually."
    if record_type == "summary":
        return "Chapter summary is excluded from lesson-step evidence."
    if record_type == "hint":
        return "Hints are excluded from lesson-step evidence."
    return "Excluded by record_type rule."


if __name__ == "__main__":
    raise SystemExit(main())
