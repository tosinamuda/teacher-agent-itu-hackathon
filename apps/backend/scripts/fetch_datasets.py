"""Download the seed corpus from the Hugging Face Hub at its pinned versions, checking every file.

    PYTHONPATH=. uv run python scripts/fetch_datasets.py [--root DIR]

The curriculum, scheme of work, textbook and objective linkage that the seed chain reads are
published as two datasets, and ``dataset/datasets.lock.json`` pins each to a Hub commit. The
raters' delivered documents come from the ratings dataset the same way. Every dataset is fetched
and checked before anything is written: a file whose bytes differ from the SHA-256 its
``PROVENANCE.json`` records, a file the provenance does not list, or a file the lock gives no
place refuses the whole fetch. A file already in place that the dataset does not have is
reported and left for a person to remove.

A lock entry names the folders it places by their path in the dataset, and may carry ``include``:
the patterns of the files it takes. Only those are downloaded, checked and placed.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import tempfile
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from huggingface_hub import snapshot_download

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[3]))
LOCK = PurePosixPath("dataset/datasets.lock.json")

#: What a dataset carries beside its data.
CARD_FILES = frozenset({"PROVENANCE.json", "README.md", "LICENSE.md", ".gitattributes"})

#: The Hub's own bookkeeping inside a downloaded snapshot.
HUB_CACHE = ".cache"

#: Finder writes this into any folder it shows; it is never part of a dataset.
DESKTOP_JUNK = frozenset({".DS_Store"})


@dataclass(frozen=True)
class Pinned:
    repo: str
    revision: str
    places: dict[str, str]
    include: tuple[str, ...] = ()

    def takes(self, path: str) -> bool:
        return not self.include or any(fnmatch.fnmatchcase(path, pat) for pat in self.include)

    def place_of(self, path: str) -> str | None:
        """The folder of the lock that holds this dataset path: the longest one that contains it."""
        held = [folder for folder in self.places if path.startswith(f"{folder}/")]
        return max(held, key=len, default=None)


@dataclass(frozen=True)
class Fetched:
    pinned: Pinned
    folder: Path
    digests: dict[str, str]


def load_lock(root: Path) -> list[Pinned]:
    entries = json.loads((root / LOCK).read_text(encoding="utf-8"))["datasets"]
    return [
        Pinned(
            entry["repo"], entry["revision"], dict(entry["places"]), tuple(entry.get("include", ()))
        )
        for entry in entries
    ]


def fetch(pinned: Pinned, into: Path, snapshot: Callable[..., str]) -> Fetched:
    folder = into / pinned.repo.replace("/", "--")
    snapshot(
        repo_id=pinned.repo,
        repo_type="dataset",
        revision=pinned.revision,
        local_dir=str(folder),
        allow_patterns=[*pinned.include, "PROVENANCE.json"] if pinned.include else None,
    )
    record = json.loads((folder / "PROVENANCE.json").read_text(encoding="utf-8"))
    digests = {e["path"]: e["sha256"] for e in record["files"] if pinned.takes(e["path"])}
    return Fetched(pinned, folder, digests)


def problems(fetched: Fetched) -> list[str]:
    """Everything that makes a fetched dataset unfit to place."""
    name = fetched.pinned.repo
    unplaced = sorted(
        _top_folders(p for p in fetched.digests if fetched.pinned.place_of(p) is None)
    )
    found = [f"{name}: {folder} has no place in {LOCK}" for folder in unplaced]
    for path, digest in sorted(fetched.digests.items()):
        file = fetched.folder / path
        if not file.is_file():
            found.append(f"{name}: {path} is listed but was not downloaded")
        elif hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            found.append(f"{name}: {path} differs from its recorded SHA-256")
    unlisted = sorted(_downloaded(fetched.folder) - fetched.digests.keys() - CARD_FILES)
    found += [f"{name}: {path} was downloaded but is not in PROVENANCE.json" for path in unlisted]
    return found


def place(fetched: Fetched, root: Path) -> list[str]:
    """Write every file where the lock places its folder; return what is in place but not in it."""
    pinned = fetched.pinned
    for path in fetched.digests:
        folder = pinned.place_of(path)
        assert folder is not None
        target = root / pinned.places[folder] / path.removeprefix(f"{folder}/")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fetched.folder / path, target)
    stale: list[str] = []
    for folder, destination in pinned.places.items():
        prefix = f"{folder}/"
        expected = {p.removeprefix(prefix) for p in fetched.digests if p.startswith(prefix)}
        present = {p for p in _files_under(root / destination) if pinned.takes(prefix + p)}
        stale += [f"{destination}/{path}" for path in sorted(present - expected)]
    return stale


def main(argv: list[str] | None = None, snapshot: Callable[..., str] = snapshot_download) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as scratch:
        fetched = [fetch(pinned, Path(scratch), snapshot) for pinned in load_lock(args.root)]
        found = [problem for item in fetched for problem in problems(item)]
        if found:
            _print(found, f"refused: {len(found)} problem(s), and nothing was written")
            return 1
        stale: list[str] = []
        for item in fetched:
            stale += place(item, args.root)
            print(f"{item.pinned.repo} at {item.pinned.revision[:12]}: {len(item.digests)} files")
    if stale:
        _print(
            stale, f"{len(stale)} file(s) in place are not in the pinned datasets; left as they are"
        )
        return 1
    return 0


def _top_folders(paths: Iterable[str]) -> set[str]:
    return {PurePosixPath(path).parts[0] for path in paths}


def _downloaded(folder: Path) -> set[str]:
    return {path for path in _files_under(folder) if PurePosixPath(path).parts[0] != HUB_CACHE}


def _files_under(folder: Path) -> set[str]:
    if not folder.is_dir():
        return set()
    return {
        path.relative_to(folder).as_posix()
        for path in folder.rglob("*")
        if path.is_file() and path.name not in DESKTOP_JUNK
    }


def _print(lines: list[str], summary: str) -> None:
    for line in lines[:25]:
        print(f"  {line}")
    print(summary)


if __name__ == "__main__":
    raise SystemExit(main())
