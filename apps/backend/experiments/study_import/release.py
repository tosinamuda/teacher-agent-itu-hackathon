"""The published study this code imports, pinned so every host imports the same bytes.

Each dataset is pinned twice: to the Hub commit it is fetched at, and to the SHA-256 of its
``PROVENANCE.json``. Every file the import reads is checked against that record, so a copy
whose record matches the pin is the release to the byte, wherever it came from. The importer
is pinned too, by a digest of its own source, so a host can tell a study imported by older
code from one imported by this.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from app.domains.experiments.domain.study_release import hub_repo
from experiments.study_import.dataset import LESSON_PLANS, RATINGS, DatasetMismatchError


@dataclass(frozen=True)
class PinnedDataset:
    name: str
    revision: str
    provenance_sha256: str
    #: Only what the import reads; the rest of the dataset is never fetched.
    reads: tuple[str, ...]


RELEASE: tuple[PinnedDataset, ...] = (
    PinnedDataset(
        LESSON_PLANS,
        revision="12db93ae9f164f2c8f502c77d05970259b2caa3b",
        provenance_sha256="f6fbde6bc5939322b25e0e3c76fc67b994741318ddeaac691a06421dcd2b667f",
        reads=("PROVENANCE.json", "notes/**", "transcripts/*/classwork.xml", "transcripts/*/*.md"),
    ),
    PinnedDataset(
        RATINGS,
        revision="7e8329bd6d6ce25ce00195faaf97673005897da5",
        provenance_sha256="8449bf2d89015138271ae1dcefc5d593cb36890d65524b07758580072cd18586",
        reads=(
            "PROVENANCE.json",
            "inputs/eval_set.json",
            "runs/h1/c0c3-prism-objective/run.json",
            "runs/h2/h2-deepseek-clean/run.json",
            "ratings/*.csv",
            "ratings/allocation/h2.xlsx",
            "ratings/delivered/**",
        ),
    ),
)


def release_record(release: tuple[PinnedDataset, ...] = RELEASE) -> dict[str, dict[str, str]]:
    """The pins as an import records them."""
    return {
        pinned.name: {"revision": pinned.revision, "provenance_sha256": pinned.provenance_sha256}
        for pinned in release
    }


def importer_digest() -> str:
    """The SHA-256 of the importer's source files, in name order."""
    digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob("*.py")):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def check_pinned(root: Path, release: tuple[PinnedDataset, ...] = RELEASE) -> Path:
    """The folder, if each dataset in it carries the pinned record; refused otherwise."""
    for pinned in release:
        provenance = root / pinned.name / "PROVENANCE.json"
        if not provenance.is_file():
            raise DatasetMismatchError(f"{provenance} is missing")
        found = hashlib.sha256(provenance.read_bytes()).hexdigest()
        if found != pinned.provenance_sha256:
            raise DatasetMismatchError(
                f"{pinned.name} is not the pinned release: its PROVENANCE.json is {found[:12]}, "
                f"not {pinned.provenance_sha256[:12]}"
            )
    return root


def fetch_release(into: Path, release: tuple[PinnedDataset, ...] = RELEASE) -> Path:
    """Download what the import reads, at the pinned commits, and check it is the release.

    The datasets are gated: the Hub token in ``HF_TOKEN`` must belong to an account with access.
    """
    from huggingface_hub import snapshot_download

    for pinned in release:
        snapshot_download(
            repo_id=hub_repo(pinned.name),
            repo_type="dataset",
            revision=pinned.revision,
            local_dir=str(into / pinned.name),
            allow_patterns=list(pinned.reads),
        )
    return check_pinned(into, release)
