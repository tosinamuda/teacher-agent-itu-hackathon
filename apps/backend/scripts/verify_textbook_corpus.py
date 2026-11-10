"""Verify linked textbook corpus consistency before seeding.

Usage:
    cd apps/backend
    uv run python scripts/verify_textbook_corpus.py
    uv run python scripts/verify_textbook_corpus.py --packet packet-0001
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # apps/backend root

from scripts.textbook_corpus_lib import verify_corpus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", dest="packet_id", default=None)
    parser.add_argument(
        "--report-path",
        default="/tmp/textbook_corpus_verification_report.json",
        help="Where to write the JSON verification report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = verify_corpus(packet_id=args.packet_id)
    report_path = Path(args.report_path)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    print(f"\nreport_path={report_path}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
