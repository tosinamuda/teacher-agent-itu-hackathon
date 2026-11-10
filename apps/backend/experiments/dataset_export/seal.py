"""Replace every published digest of an original with the same digest of its published form.

A replacement changes the file it is made in, and that file's original is then one more
whose digests must not be published, so replacement repeats until a round finds none.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from itertools import chain
from pathlib import PurePosixPath

from . import digests
from .build import Entry, Release
from .rewrite import TEXT_SUFFIXES, ExportError


def seal(releases: Iterable[Release]) -> dict[str, str]:
    """Replace digests of originals across every dataset at once; return what replaced what."""
    entries = [entry for release in releases for entry in release.entries]
    runs = [hex_runs(entry) for entry in entries]
    replaced: dict[str, str] = {}
    while found := digests.swaps(set().union(*runs), candidates(entries)):
        again = sorted(replaced.keys() & found.keys())
        if again:
            raise ExportError(f"{again[0]}: replaced once and found again")
        for index, entry in enumerate(entries):
            if not runs[index].isdisjoint(found):
                _replace(entry, found)
                runs[index] = hex_runs(entry)
        replaced |= found
    return replaced


def candidates(entries: Iterable[Entry]) -> Iterator[digests.Pair]:
    """Every digest a recorder might have taken of the original of a file the export changed."""
    return chain.from_iterable(
        digests.pairs(entry.original, entry.body, entry.landed)
        for entry in entries
        if entry.body != entry.original
    )


def hex_runs(entry: Entry) -> set[str]:
    runs = digests.hex_runs(entry.path)
    if is_text(entry.path):
        runs |= digests.hex_runs(entry.body.decode("utf-8"))
    return runs


def is_text(path: str) -> bool:
    return PurePosixPath(path).suffix in TEXT_SUFFIXES


def _replace(entry: Entry, found: dict[str, str]) -> None:
    entry.path = digests.translate(entry.path, found)
    if is_text(entry.path):
        entry.body = digests.translate(entry.body.decode("utf-8"), found).encode("utf-8")
