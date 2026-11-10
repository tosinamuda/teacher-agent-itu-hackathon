"""Where a harness run writes: a folder of its own, named for when it started.

A run named only for its settings shared a folder with every earlier run of the same
settings, and the later one truncated the earlier one's traces and rewrote its record. Each
new run now gets ``<stem>-<UTC start>``; carrying on with an interrupted run is asked for by
name with ``--resume``, and is the only way a run writes into a folder that already exists.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def run_label(stem: str, started: datetime) -> str:
    """The name of a run that began at ``started``: sortable, and unique to the second."""
    return f"{stem}-{started.astimezone(timezone.utc):%Y%m%dT%H%M%SZ}"


def open_run(runs: Path, *, stem: str, resume: str | None) -> tuple[str, Path]:
    """The run's label and folder: a new one, or the interrupted one named by ``resume``."""
    if resume is not None:
        folder = runs / resume
        if not folder.is_dir():
            raise SystemExit(f"there is no run {resume!r} under {runs} to resume")
        return resume, folder
    label = run_label(stem, datetime.now(timezone.utc))
    folder = runs / label
    try:
        folder.mkdir(parents=True)
    except FileExistsError:
        raise SystemExit(
            f"{folder} already exists: another run started this second; start again"
        ) from None
    return label, folder


def add_run_arguments(parser: argparse.ArgumentParser, *, stem_help: str) -> None:
    """The two options every harness takes for where its run goes."""
    parser.add_argument("--label", help=f"{stem_help}; the start time is added to it")
    parser.add_argument(
        "--resume", metavar="LABEL", help="carry on with the interrupted run of this full label"
    )
