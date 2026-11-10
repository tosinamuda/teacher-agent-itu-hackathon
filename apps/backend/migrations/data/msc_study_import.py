"""Bring the MSc study into the database as published, and keep it as the code pins it.

Idempotent. A database whose import record matches the pinned release and the importer's
digest is left alone. Otherwise the release is fetched at its pinned commits, checked file by
file, and imported; a study imported earlier, from another release or by other code, is
withdrawn and imported again in the same transaction. Every host that runs it holds the same
study.
"""

from __future__ import annotations

import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.infrastructure.models import Investigation
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from experiments.study_import.dataset import ReleasedStudy
from experiments.study_import.importer import ImportReport, import_study
from experiments.study_import.release import fetch_release, importer_digest, release_record
from experiments.study_import.runs import INVESTIGATION_ID

#: Puts the release in the folder it is given and returns the folder holding both datasets.
Source = Callable[[Path], Path]


@dataclass(frozen=True)
class Outcome:
    action: str
    report: ImportReport | None = None


async def bring_in_the_study(
    db: AsyncSession, source: Source = fetch_release, *, commit: bool = True
) -> Outcome:
    """Import the pinned study, or replace an import that differs from it; else do nothing."""
    wanted = StudyImport(
        investigation_id=INVESTIGATION_ID,
        release=release_record(),
        importer=importer_digest(),
    )
    stored = await db.scalar(
        select(StudyImport).where(StudyImport.investigation_id == INVESTIGATION_ID)
    )
    if stored is not None and (stored.release, stored.importer) == (
        wanted.release,
        wanted.importer,
    ):
        return Outcome("up to date")
    present = stored is not None or await db.scalar(
        select(Investigation.id).where(Investigation.investigation_id == INVESTIGATION_ID)
    )
    with tempfile.TemporaryDirectory() as scratch:
        study = ReleasedStudy(source(Path(scratch)))
        report = await import_study(db, study, commit=commit, replace=bool(present), record=wanted)
    return Outcome("replaced" if present else "imported", report)
