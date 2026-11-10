"""Run active parsers to generate processed curriculum intermediates.

Usage:
    cd apps/backend
    uv run python scripts/parsers/run_all.py
"""

import importlib
import sys
from pathlib import Path

# Ensure the parsers package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> None:
    print("=" * 60)
    print("Running all parsers...")
    print("=" * 60)
    print()

    parse_curriculum = importlib.import_module("parse_curriculum")
    parse_curriculum.main()
    print()

    parse_scheme = importlib.import_module("parse_scheme_of_work")
    parse_scheme.main()
    print()

    print("Skipping textbook parser.")
    print("The prototype now consumes the record-level linked textbook corpus")
    print("from dataset/processed/textbook/jsonl/linked instead.")
    print()

    print("=" * 60)
    print("All parsers complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
