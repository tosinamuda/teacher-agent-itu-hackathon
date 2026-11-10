"""Check the built datasets before any of it leaves this machine.

The rewrite decides what changes; this confirms the result. It reads every file the way a
reuser would — text as text, a PDF through its extracted text, a Word or Excel document
through the XML inside it — because a rule having been applied is not the same thing as a
release being clean.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from . import digests
from .build import Release, provenance
from .rewrite import CAPTURES, CLASSWORK_WARNING, TEXT_SUFFIXES
from .seal import candidates
from .sources import PHOTOGRAPHS

SCHOOL_WORD = re.compile(r"\bgtc\b", re.IGNORECASE)
SCHOOL_LETTERS = re.compile(r"gtc", re.IGNORECASE)
ZIPPED = frozenset({".docx", ".pptx", ".xlsx"})

#: Three letters inside a run of at least this many word characters belong to an opaque id —
#: a tool-call id, a digest — and are chance rather than the school.
OPAQUE_ID_LENGTH = 12

#: Files a build adds beside what it copies.
BUILD_FILES = frozenset({"PROVENANCE.json", "README.md", "LICENSE.md"})


@dataclass
class Report:
    dataset: str
    files: int = 0
    unread: dict[str, int] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)
    #: Every hex run read anywhere in the dataset, with the files it was read in.
    hex_runs: dict[str, set[str]] = field(default_factory=dict)


def verify(root: Path) -> Report:
    record = root / "PROVENANCE.json"
    if not record.exists():
        return Report(root.name, problems=[f"{root}: not built"])
    recorded = json.loads(record.read_text(encoding="utf-8"))
    report = Report(recorded["dataset"])
    listed = {entry["path"] for entry in recorded["files"]}
    on_disk = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    for stray in sorted(on_disk - listed - BUILD_FILES):
        report.problems.append(f"{stray}: on disk but not in PROVENANCE.json")
    for entry in recorded["files"]:
        report.files += 1
        _check(root, entry, report)
    for name in sorted(BUILD_FILES & on_disk):
        _check_text(name, (root / name).read_text(encoding="utf-8"), report)
    return report


def against(release: Release, root: Path) -> list[str]:
    """Where the recorded dataset differs from what its sources produce now."""
    record = root / "PROVENANCE.json"
    if not record.exists():
        return []
    recorded = json.loads(record.read_text(encoding="utf-8"))
    expected = provenance(release)
    problems = [
        f"PROVENANCE.json: '{key}' differs from what the sources produce"
        for key in expected
        if key != "files" and recorded.get(key) != expected[key]
    ]
    was = {entry["path"]: entry["sha256"] for entry in recorded["files"]}
    now = {entry["path"]: entry["sha256"] for entry in expected["files"]}
    problems += [f"{path}: no longer produced by the sources" for path in sorted(was - now.keys())]
    problems += [f"{path}: produced by the sources, not built" for path in sorted(now - was.keys())]
    problems += [
        f"{path}: differs from what the sources produce"
        for path in sorted(was.keys() & now.keys())
        if was[path] != now[path]
    ]
    return problems


def leaks(reports: Iterable[Report], releases: Iterable[Release]) -> list[str]:
    """Hex runs read anywhere in the release that begin a digest of an original."""
    places: dict[str, set[str]] = {}
    for report in reports:
        for run, names in report.hex_runs.items():
            places.setdefault(run, set()).update(f"{report.dataset}/{name}" for name in names)
    entries = [entry for release in releases for entry in release.entries]
    found = digests.swaps(set(places), candidates(entries))
    return [
        f"{run} begins a digest of an original, in {', '.join(sorted(places[run])[:3])}"
        for run in sorted(found)
    ]


def _check(root: Path, entry: dict[str, object], report: Report) -> None:
    name = str(entry["path"])
    path = root / name
    body = path.read_bytes()
    if hashlib.sha256(body).hexdigest() != entry["sha256"]:
        report.problems.append(f"{name}: bytes differ from the recorded digest")
    if name.endswith(tuple(PHOTOGRAPHS)):
        report.problems.append(f"{name}: a photograph is in the release")
    _check_text(f"{name} (its name)", name, report)
    text = _readable_text(path, body)
    if text is None:
        suffix = path.suffix.lower()
        report.unread[suffix] = report.unread.get(suffix, 0) + 1
        return
    _check_text(name, text, report)


def _check_text(name: str, text: str, report: Report) -> None:
    if SCHOOL_WORD.search(text):
        report.problems.append(f"{name}: the school's abbreviation is still there")
    elif any(not _inside_opaque_id(text, match) for match in SCHOOL_LETTERS.finditer(text)):
        report.problems.append(f"{name}: 'gtc' appears outside an opaque id")
    if CAPTURES in text:
        report.problems.append(f"{name}: names the private captures folder")
    if PurePosixPath(name).name == "classwork.xml" and CLASSWORK_WARNING in text:
        report.problems.append(f"{name}: still carries the never-leave-this-repository warning")
    for run in digests.hex_runs(text):
        report.hex_runs.setdefault(run, set()).add(name)


def _readable_text(path: Path, body: bytes) -> str | None:
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return body.decode("utf-8")
    if suffix == ".pdf":
        return _pdf_text(path)
    if suffix in ZIPPED:
        return _zipped_text(path)
    return None


def _pdf_text(path: Path) -> str:
    if shutil.which("pdftotext") is None:
        raise RuntimeError("pdftotext is required to verify PDFs; install poppler")
    return subprocess.run(
        ["pdftotext", str(path), "-"], check=True, capture_output=True, text=True
    ).stdout


def _zipped_text(path: Path) -> str:
    """The text inside an Office document, with tags removed and no space put in their place.

    Word splits a word across runs wherever its formatting changes, so a tag can fall in the
    middle of one; replacing tags with spaces would split the very words being looked for.
    """
    with zipfile.ZipFile(path) as archive:
        parts = [
            archive.read(member).decode("utf-8", "ignore")
            for member in archive.namelist()
            if member.endswith(".xml")
        ]
    return re.sub(r"<[^>]+>", "", "\n".join(parts))


def _inside_opaque_id(text: str, match: re.Match[str]) -> bool:
    left, right = match.start(), match.end()
    while left > 0 and (text[left - 1].isalnum() or text[left - 1] == "_"):
        left -= 1
    while right < len(text) and (text[right].isalnum() or text[right] == "_"):
        right += 1
    return right - left >= OPAQUE_ID_LENGTH
