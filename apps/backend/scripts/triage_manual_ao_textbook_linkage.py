"""Generate review-triage metadata for manual AO-textbook linkage rows.

This script does not decide textbook-to-AO linkage. It reads already-authored
manual linkage rows and classifies why rows are still marked needs_review or
no_records so expert review can be targeted.

Usage:
    uv run python scripts/triage_manual_ao_textbook_linkage.py
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import cast

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

DEFAULT_LINKAGE_DIR = PROJECT_ROOT / "dataset" / "processed" / "ao_textbook_linkage" / "manual"
DEFAULT_OUTPUT_PATH = DEFAULT_LINKAGE_DIR / "review_triage.json"


def main() -> int:
    from app.domains.expert_content.application import (
        build_manual_linkage_review_triage_report,
    )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--linkage-dir",
        default=str(DEFAULT_LINKAGE_DIR),
        help="Directory containing manual linkage row JSON files and manifest.json.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Path to write the review triage JSON report.",
    )
    parser.add_argument(
        "--generated-at",
        default=date.today().isoformat(),
        help="Date stamp to embed in the generated report.",
    )
    args = parser.parse_args()

    linkage_dir = Path(args.linkage_dir)
    output_path = Path(args.output)
    row_payloads = _load_row_payloads(linkage_dir)
    report = build_manual_linkage_review_triage_report(
        row_payloads,
        generated_at=str(args.generated_at),
    )
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_path": str(output_path),
                "row_count": report["row_count"],
                "status_counts": report["status_counts"],
                "category_counts": report["category_counts"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _load_row_payloads(linkage_dir: Path) -> list[dict[str, object]]:
    manifest_path = linkage_dir / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"Missing manual linkage manifest: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest.get("rows")
    if not isinstance(rows, list):
        raise ValueError("manual linkage manifest rows must be a list")

    row_payloads: list[dict[str, object]] = []
    for manifest_row in rows:
        if not isinstance(manifest_row, dict):
            continue
        row_path = PROJECT_ROOT / str(manifest_row.get("path") or "")
        row_payloads.append(
            cast(
                dict[str, object],
                json.loads(row_path.read_text(encoding="utf-8")),
            )
        )
    return row_payloads


if __name__ == "__main__":
    raise SystemExit(main())
