"""Write every arm's snapshot, and the provenance map, to disk."""

from __future__ import annotations

from pathlib import Path

from scripts.prompt_snapshots import PROVENANCE_PATH, SERVED_DIR, SNAPSHOT_DIR
from scripts.prompt_snapshots.arms import every_arm
from scripts.prompt_snapshots.provenance import provenance_table
from scripts.prompt_snapshots.render import (
    PROVENANCE_HEADER,
    served_snapshot_text,
    snapshot_name,
    snapshot_text,
)
from scripts.prompt_snapshots.served import every_served_arm


def _write(path: Path, text: str) -> None:
    changed = not path.exists() or path.read_text(encoding="utf-8") != text
    path.write_text(text, encoding="utf-8")
    print(f"{'wrote' if changed else 'unchanged'} {path.relative_to(SNAPSHOT_DIR.parents[2])}")


def main() -> int:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    for arm in every_arm():
        _write(SNAPSHOT_DIR / snapshot_name(arm), snapshot_text(arm))
    SERVED_DIR.mkdir(exist_ok=True)
    for served in every_served_arm():
        _write(SERVED_DIR / snapshot_name(served), served_snapshot_text(served))
    _write(PROVENANCE_PATH, PROVENANCE_HEADER + provenance_table() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
