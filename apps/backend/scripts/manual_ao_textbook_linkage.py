"""Prepare and validate manual AO-to-textbook linkage for one subtopic.

Examples:
    uv run python scripts/manual_ao_textbook_linkage.py \
        --subtopic-id jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa \
        --output-dir ../../dataset/processed/ao_textbook_linkage/manual/fractions-pilot-inputs

    uv run python scripts/manual_ao_textbook_linkage.py \
        --subtopic-id jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa \
        --validate-row ../../dataset/processed/ao_textbook_linkage/manual/fractions-pilot.json
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

DEFAULT_ATOMIC_OBJECTIVES_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "processed"
    / "curriculum"
    / "manual_authoring"
    / "jss1-math_atomic_objectives_all_topics.jsonl"
)
DEFAULT_PROMPT_TEMPLATE_PATH = Path(__file__).with_name("manual_ao_textbook_linkage_prompt.md")


def _parse_args() -> argparse.Namespace:
    from scripts.textbook_corpus_lib import linked_records_path

    parser = argparse.ArgumentParser(
        description="Prepare prompt inputs and validate manual AO-textbook linkage rows.",
    )
    parser.add_argument("--subtopic-id", required=True, help="Target curriculum subtopic_id.")
    parser.add_argument(
        "--atomic-objectives",
        default=str(DEFAULT_ATOMIC_OBJECTIVES_PATH),
        help="Path to the atomic-objective JSONL source.",
    )
    parser.add_argument(
        "--records",
        default=str(linked_records_path()),
        help="Path to the linked textbook records JSONL source.",
    )
    parser.add_argument(
        "--prompt-template",
        default=str(DEFAULT_PROMPT_TEMPLATE_PATH),
        help="Path to the corrected manual-linkage prompt template.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Optional directory to write atomic_objectives.json, textbook_records.json, "
            "prompt.md, and manifest.json."
        ),
    )
    parser.add_argument(
        "--validate-row",
        default=None,
        help="Optional path to a returned linkage row JSON file to validate.",
    )
    parser.add_argument(
        "--validation-summary-path",
        default=None,
        help="Optional path to write the validation summary JSON.",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the rendered prompt to stdout.",
    )
    return parser.parse_args()


def main() -> int:
    from app.domains.expert_content.application.linkage_inference import (
        build_manual_ao_textbook_linkage_prompt,
        flatten_atomic_objectives,
        load_reduced_subtopic_textbook_records,
        load_subtopic_atomic_objective_source,
    )
    from app.domains.expert_content.application.linkage_validation import (
        validate_manual_linkage_row,
    )

    args = _parse_args()

    atomic_path = Path(args.atomic_objectives)
    records_path = Path(args.records)
    prompt_template_path = Path(args.prompt_template)

    atomic_objective_source = load_subtopic_atomic_objective_source(
        atomic_path,
        args.subtopic_id,
    )
    textbook_records = load_reduced_subtopic_textbook_records(
        records_path,
        args.subtopic_id,
    )
    prompt_text = build_manual_ao_textbook_linkage_prompt(
        template_text=prompt_template_path.read_text(encoding="utf-8"),
        atomic_objective_source=atomic_objective_source,
        textbook_records=textbook_records,
    )

    summary = {
        "subtopic_id": args.subtopic_id,
        "subtopic_title": atomic_objective_source.get("subtopic_title"),
        "atomic_objective_count": len(flatten_atomic_objectives(atomic_objective_source)),
        "textbook_record_count": len(textbook_records),
        "prompt_template_path": str(prompt_template_path),
        "atomic_objectives_path": str(atomic_path),
        "records_path": str(records_path),
    }

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "atomic_objectives.json").write_text(
            json.dumps(atomic_objective_source, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (output_dir / "textbook_records.json").write_text(
            json.dumps(textbook_records, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (output_dir / "prompt.md").write_text(prompt_text, encoding="utf-8")
        (output_dir / "manifest.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.print_prompt or (not args.output_dir and not args.validate_row):
        print(prompt_text)

    if args.validate_row:
        row_payload = json.loads(Path(args.validate_row).read_text(encoding="utf-8"))
        report = validate_manual_linkage_row(
            row_payload=row_payload,
            atomic_objective_source=atomic_objective_source,
            textbook_records=textbook_records,
        )
        report_json = report.as_json()
        if args.validation_summary_path:
            Path(args.validation_summary_path).write_text(
                json.dumps(report_json, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        print(json.dumps(report_json, ensure_ascii=False, indent=2))
        return 0 if report.valid else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
