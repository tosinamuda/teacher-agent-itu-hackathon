"""Digests of what the export changed, so that no digest of an original is published.

The school's abbreviation is three letters. A release that carries a rewritten file beside
any digest of that file's original gives the abbreviation back: put each of the 17,576
three-letter strings where the replacement stands, hash, and compare. The study records
digests of exactly such files — each session plan's text cut to sixteen hex characters in
the eval set and in every run, a digest of that in every fingerprint, and the plan digest
again in the name of each superseded plan. So every digest a recorder could have taken of
an original is paired here with the same digest of its published form, which replaces it.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Iterator
from pathlib import PurePosixPath
from typing import Any

from .rewrite import ExportError

#: A run of hex digits long enough to be a truncated digest, with no hex digit either side.
HEX_RUN = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{8,64}(?![0-9A-Fa-f])")

#: Shorter runs are everywhere in ordinary text — numbers, colours, words like "facade" —
#: and the study's only shorter digests are of generated material, which never held the
#: abbreviation.
SHORTEST = 8

ALGORITHMS = ("sha256", "sha1", "md5", "blake2b")

#: How JSON is serialised before it is hashed: session plans as written, and sorted keys.
JSON_FORMS: tuple[dict[str, Any], ...] = (
    {"indent": 2, "ensure_ascii": False},
    {"indent": 2},
    {"sort_keys": True},
    {"sort_keys": True, "separators": (",", ":")},
    {},
)

#: Keys the eval set adds to a plan after its digest is taken. The transcripts never carry the
#: ``sets_work`` judgement, so a frozen plan's digest is of the plan without it — and anyone
#: comparing a frozen plan with its session plan can see exactly what to strip.
ADDED_AFTER_DIGEST = frozenset({"sets_work"})

Pair = tuple[str, str]


def pairs(original: bytes, published: bytes, path: str) -> Iterator[Pair]:
    """Each digest a recorder might have taken of the original, beside the published form's.

    Beyond the file's own digests: every changed JSON value under each serialisation, and a
    digest of every truncation of each of those, which is how a run fingerprints a plan.
    """
    for before, after in _first_order(original, published, path):
        yield before, after
        for length in range(SHORTEST, len(before) + 1):
            yield _sha256(before[:length]), _sha256(after[:length])


def _first_order(original: bytes, published: bytes, path: str) -> Iterator[Pair]:
    for name in ALGORITHMS:
        yield hashlib.new(name, original).hexdigest(), hashlib.new(name, published).hexdigest()
    yield _git_blob(original), _git_blob(published)
    if PurePosixPath(path).suffix == ".json":
        yield from _json_pairs(original, published)


def _json_pairs(original: bytes, published: bytes) -> Iterator[Pair]:
    try:
        before, after = json.loads(original), json.loads(published)
    except ValueError:
        return
    for old, new in _changed_values(before, after):
        if isinstance(old, str) and isinstance(new, str):
            yield _sha256(old), _sha256(new)
            continue
        for old_value, new_value in _as_digested(old, new):
            for form in JSON_FORMS:
                old_text, new_text = json.dumps(old_value, **form), json.dumps(new_value, **form)
                yield _sha256(old_text), _sha256(new_text)
                yield _sha256(f"{old_text}\n"), _sha256(f"{new_text}\n")


def _as_digested(old: Any, new: Any) -> Iterator[tuple[Any, Any]]:
    """The value, and the value as it stood before the eval set added its judgements to it."""
    yield old, new
    stripped = _without(old, ADDED_AFTER_DIGEST), _without(new, ADDED_AFTER_DIGEST)
    if stripped != (old, new):
        yield stripped


def _without(value: Any, keys: frozenset[str]) -> Any:
    if isinstance(value, dict):
        return {key: _without(item, keys) for key, item in value.items() if key not in keys}
    if isinstance(value, list):
        return [_without(item, keys) for item in value]
    return value


def _changed_values(old: Any, new: Any) -> Iterator[tuple[Any, Any]]:
    if old == new:
        return
    yield old, new
    if isinstance(old, dict) and isinstance(new, dict):
        for old_value, new_value in zip(old.values(), new.values(), strict=True):
            yield from _changed_values(old_value, new_value)
    elif isinstance(old, list) and isinstance(new, list):
        for old_item, new_item in zip(old, new, strict=True):
            yield from _changed_values(old_item, new_item)


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hex_runs(text: str) -> set[str]:
    return {match.group(0).lower() for match in HEX_RUN.finditer(text)}


def swaps(published: set[str], candidates: Iterable[Pair]) -> dict[str, str]:
    """Each published hex run that begins a digest of an original, and what replaces it."""
    by_head: dict[str, list[str]] = {}
    for run in published:
        by_head.setdefault(run[:SHORTEST], []).append(run)
    found: dict[str, str] = {}
    for before, after in candidates:
        for run in by_head.get(before[:SHORTEST], ()):
            if not before.startswith(run):
                continue
            replacement = after[: len(run)]
            if found.setdefault(run, replacement) != replacement:
                raise ExportError(f"{run}: begins digests of two different originals")
    return found


def translate(text: str, found: dict[str, str]) -> str:
    """The text with each hex run in ``found`` replaced, keeping its case."""
    return HEX_RUN.sub(lambda match: _replacement(match.group(0), found), text)


def _replacement(run: str, found: dict[str, str]) -> str:
    replacement = found.get(run.lower(), run)
    return replacement.upper() if run.isupper() else replacement
