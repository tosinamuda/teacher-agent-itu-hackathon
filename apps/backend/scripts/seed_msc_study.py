"""Bring the MSc study into the database, as the code pins it.

Invocation::

    uv run python -m scripts.seed_msc_study [--from <folder>] [--dry-run]

Fetches the two gated datasets at their pinned commits (``HF_TOKEN``, from the environment or
``.env``, must hold a token with access), or reads a local copy with ``--from``, which is
refused unless it is the pinned release. Idempotent: a database already holding the pinned
study, imported by this code, is left alone. ``--dry-run`` does everything and rolls it back.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import asdict
from pathlib import Path

import app.db.metadata  # noqa: F401  (every model, so each mapper can resolve the rest)
from app.db.session import AsyncSessionLocal, engine
from experiments.study_import.dataset import DatasetMismatchError
from experiments.study_import.release import check_pinned, fetch_release
from experiments.study_import.school import CurriculumNotSeededError
from migrations.data.msc_study_import import Outcome, Source, bring_in_the_study


async def _run(source: Source, *, dry_run: bool) -> Outcome:
    try:
        async with AsyncSessionLocal() as db:
            return await bring_in_the_study(db, source, commit=not dry_run)
    finally:
        await engine.dispose()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--from", dest="folder", type=Path, help="a local copy of the release")
    parser.add_argument("--dry-run", action="store_true", help="do it all, then roll it back")
    arguments = parser.parse_args()
    folder: Path | None = arguments.folder
    source: Source = (lambda _: check_pinned(folder)) if folder else fetch_release
    try:
        outcome = asyncio.run(_run(source, dry_run=arguments.dry_run))
    except (CurriculumNotSeededError, DatasetMismatchError) as refusal:
        print(f"msc study not imported: {refusal}", file=sys.stderr)
        return 1
    counts = asdict(outcome.report) if outcome.report else {}
    verb = f"would be {outcome.action}" if arguments.dry_run and outcome.report else outcome.action
    print(f"msc study {verb}" + "".join(f", {k.replace('_', ' ')} {v}" for k, v in counts.items()))
    return 0


if __name__ == "__main__":
    from app.environment import prepare_environment

    prepare_environment()
    sys.exit(main())
