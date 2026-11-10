"""The study is brought in as the code pins it: once, then left alone until the pin changes."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.infrastructure.models import ExperimentConditionRun
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from experiments.study_import.dataset import LESSON_PLANS, RATINGS, DatasetMismatchError
from experiments.study_import.release import PinnedDataset, check_pinned
from migrations.data import msc_study_import
from migrations.data.msc_study_import import bring_in_the_study
from tests.study_release import seed_curriculum, write_release


def _pins(root: Path) -> tuple[PinnedDataset, ...]:
    """Pins for a folder, as the code pins the real release."""
    return tuple(
        PinnedDataset(
            name,
            revision="0" * 40,
            provenance_sha256=hashlib.sha256(
                (root / name / "PROVENANCE.json").read_bytes()
            ).hexdigest(),
            reads=("**",),
        )
        for name in (LESSON_PLANS, RATINGS)
    )


def _never(_: Path) -> Path:
    raise AssertionError("the release was fetched for a database already up to date")


async def _runs(db: AsyncSession) -> int:
    return int(await db.scalar(select(func.count()).select_from(ExperimentConditionRun)) or 0)


@pytest.mark.asyncio
async def test_the_study_is_brought_in_once_and_then_left_alone(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_curriculum(db)
    root = write_release(tmp_path)

    first = await bring_in_the_study(db, lambda _: root)
    second = await bring_in_the_study(db, _never)

    assert (first.action, second.action) == ("imported", "up to date")
    assert await _runs(db) == 72 + 52
    record = await db.scalar(select(StudyImport))
    assert record is not None and set(record.release) == {LESSON_PLANS, RATINGS}


@pytest.mark.asyncio
async def test_a_study_imported_by_other_code_is_replaced_whole(
    db: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    await seed_curriculum(db)
    root = write_release(tmp_path)
    await bring_in_the_study(db, lambda _: root)
    monkeypatch.setattr(msc_study_import, "importer_digest", lambda: "a corrected importer")

    again = await bring_in_the_study(db, lambda _: root)

    assert again.action == "replaced"
    assert await _runs(db) == 72 + 52
    record = await db.scalar(select(StudyImport))
    assert record is not None and record.importer == "a corrected importer"


def test_a_copy_that_is_not_the_pinned_release_is_refused(tmp_path: Path) -> None:
    root = write_release(tmp_path)
    pins = _pins(root)
    assert check_pinned(root, pins) == root

    (root / RATINGS / "PROVENANCE.json").write_text('{"files": []}')

    with pytest.raises(DatasetMismatchError, match="is not the pinned release"):
        check_pinned(root, pins)
