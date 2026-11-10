"""Render and regenerate the committed prompt snapshots.

    uv run python -m scripts.prompt_snapshots

An intended prompt change is then a diff in `tests/snapshots/prompts/`, reviewable beside
the code that caused it. `tests/test_rendered_prompt_snapshots.py` fails when the two
disagree.
"""

from pathlib import Path

SNAPSHOT_DIR = Path(__file__).resolve().parents[2] / "tests" / "snapshots" / "prompts"
PROVENANCE_PATH = SNAPSHOT_DIR / "FIELD-PROVENANCE.md"
SERVED_DIR = SNAPSHOT_DIR / "served"
