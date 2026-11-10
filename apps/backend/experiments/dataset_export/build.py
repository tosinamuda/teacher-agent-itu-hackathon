"""Materialise the datasets from git objects, rewritten for release, with their provenance."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tarfile
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

from .rewrite import ExportError, published
from .sources import Dataset, Source


@dataclass
class Entry:
    """One file of a dataset: where its source lands it, what was committed, and what ships."""

    landed: str
    original: bytes
    body: bytes
    path: str = field(default="")
    #: The published paths a table built by the export was read from; empty for a copied file.
    derived_from: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        self.path = self.path or self.landed

    @property
    def rewritten(self) -> bool:
        return self.body != self.original or self.path != self.landed


@dataclass(frozen=True)
class Release:
    """One dataset as it will be published."""

    name: str
    sources: tuple[dict[str, str], ...]
    entries: tuple[Entry, ...]
    left_out: tuple[str, ...]


def commit_of(source: Source) -> str:
    return subprocess.run(
        ["git", "-C", str(source.repo.root), "rev-parse", f"{source.revision}^{{commit}}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def members(source: Source, commit: str) -> Iterator[tuple[str, bytes]]:
    """Every committed file under the source path, streamed out of ``git archive``."""
    command = ["git", "-C", str(source.repo.root), "archive", "--format=tar", commit, "--"]
    with subprocess.Popen([*command, source.path], stdout=subprocess.PIPE) as process:
        if process.stdout is None:
            raise ExportError("git archive produced no output stream")
        with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
            for member in archive:
                if member.issym() or member.islnk():
                    raise ExportError(f"{member.name}: links are not published")
                handle = archive.extractfile(member) if member.isfile() else None
                if handle is not None:
                    yield member.name, handle.read()
    if process.returncode:
        raise ExportError(f"git archive failed for {source.repo.name}:{source.path}")


def destination(source: Source, member: str) -> str | None:
    """Where a committed file lands in the dataset, or ``None`` if the source leaves it out."""
    if member == source.path:
        return source.lands if source.keep(PurePosixPath(member).name) else None
    relative = member.removeprefix(f"{source.path}/")
    return f"{source.lands}/{relative}" if source.keep(relative) else None


def collect(dataset: Dataset) -> Release:
    """Every file the dataset's sources commit, placed and rewritten, with nothing written."""
    sources: list[dict[str, str]] = []
    entries: list[Entry] = []
    left_out: list[str] = []
    for source in dataset.sources:
        commit = commit_of(source)
        sources.append(
            {
                "repo": source.repo.name,
                "revision": source.revision,
                "commit": commit,
                "path": source.path,
                "lands": source.lands,
            }
        )
        for member, data in members(source, commit):
            landed = destination(source, member)
            if landed is None:
                left_out.append(f"{source.repo.name}:{member}")
                continue
            body = published(landed, data)
            entries.append(Entry(landed, data, data if body == data else body))
    return Release(dataset.name, tuple(sources), tuple(entries), tuple(sorted(left_out)))


def write(release: Release, out: Path, *, replace: bool = False) -> Path:
    """Write the dataset under ``out`` with its provenance, replacing a build only when told."""
    landings = Counter(entry.path for entry in release.entries)
    clashes = sorted(path for path, count in landings.items() if count > 1)
    if clashes:
        raise ExportError(f"{release.name}: more than one file lands on {', '.join(clashes[:5])}")
    root = out / release.name
    if root.exists():
        if not replace:
            raise ExportError(f"{root} already exists; pass --replace to rebuild it")
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for entry in release.entries:
        target = root / entry.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(entry.body)
    record = json.dumps(provenance(release), indent=2) + "\n"
    (root / "PROVENANCE.json").write_text(record, encoding="utf-8")
    return root


def provenance(release: Release) -> dict[str, Any]:
    files = sorted(release.entries, key=lambda entry: entry.path)
    return {
        "dataset": release.name,
        "sources": list(release.sources),
        "file_count": len(files),
        "rewritten_count": sum(entry.rewritten for entry in files),
        "left_out": list(release.left_out),
        "files": [_file_record(entry) for entry in files],
    }


def _file_record(entry: Entry) -> dict[str, Any]:
    record: dict[str, Any] = {
        "path": entry.path,
        "sha256": hashlib.sha256(entry.body).hexdigest(),
        "rewritten": entry.rewritten,
    }
    if entry.derived_from:
        record["derived_from"] = list(entry.derived_from)
    return record
