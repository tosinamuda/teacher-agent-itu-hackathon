"""The card each dataset is published with.

The prose is written by hand in ``cards/<dataset>.<FILE>.md``. What the build decides — how
many files, how large, how many were rewritten — is filled in from the release, so a card
cannot drift from the files it describes.
"""

from __future__ import annotations

from pathlib import Path
from string import Template

import yaml

from .build import Release

TEMPLATES = Path(__file__).with_name("cards")

#: The Hub's size buckets, by the number of files a dataset holds.
SIZE_CATEGORIES = (
    (1_000, "n<1K"),
    (10_000, "1K<n<10K"),
    (100_000, "10K<n<100K"),
    (1_000_000, "100K<n<1M"),
)


def cards(release: Release, replaced: int) -> dict[str, str]:
    """The card's files by published name: its README, and a LICENSE where the README links one."""
    values = _values(release, replaced)
    return {
        template.name.removeprefix(f"{release.name}."): Template(
            template.read_text(encoding="utf-8")
        ).substitute(values)
        for template in sorted(TEMPLATES.glob(f"{release.name}.*.md"))
    }


def write_cards(release: Release, root: Path, replaced: int) -> None:
    for name, text in cards(release, replaced).items():
        (root / name).write_text(text, encoding="utf-8")


def viewer_tables(readme: str) -> list[str]:
    """The files a card asks the Hub's Dataset Viewer to read as tables, by published path."""
    metadata = yaml.safe_load(readme.removeprefix("---\n").partition("\n---\n")[0]) or {}
    return [
        split["path"] for config in metadata.get("configs", []) for split in config["data_files"]
    ]


def missing_tables(root: Path) -> list[str]:
    """Viewer tables the built dataset's card names but the dataset does not hold."""
    readme = (root / "README.md").read_text(encoding="utf-8")
    return [path for path in viewer_tables(readme) if not (root / path).is_file()]


def _values(release: Release, replaced: int) -> dict[str, str]:
    files = len(release.entries)
    size = sum(len(entry.body) for entry in release.entries)
    return {
        "file_count": f"{files:,}",
        "size": f"{size / 1_000_000:.1f} MB",
        "size_category": next(label for limit, label in SIZE_CATEGORIES if files < limit),
        "rewritten_count": f"{sum(entry.rewritten for entry in release.entries):,}",
        "digests_replaced": f"{replaced:,}",
    }
