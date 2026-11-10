"""An imported lesson, read back as generation reads it, is the input the study's Part 1 read.

The lesson plan and the lesson note are imported as separate records. Joined again, they must
build the very request Part 1 built from its frozen plan and corrected notes, for every lesson
and every condition, so a run on imported data sends Part 1's prompts byte for byte (the prompt
side is pinned by ``test_review_pack_pipelines``). The notes must also reproduce the digest
Part 1's own run recorded of them.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_note_input import (  # noqa: E501
    with_lesson_note,
)
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.note_editorial import CLEAN_DIR
from experiments.study_import.dataset import (
    LESSON_PLANS,
    RATINGS,
    DatasetMismatchError,
    ReleasedStudy,
    StudyLesson,
)
from tests.part_1_input import CONDITIONS, PART_1, RELEASE, RUN, part_1_inputs, part_1_request


def _provenance(root: Path) -> None:
    files = [
        {
            "path": str(path.relative_to(root)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]
    (root / "PROVENANCE.json").write_text(json.dumps({"files": files}))


@pytest.fixture
def repo_release(tmp_path: Path) -> Path:
    """The two datasets' study files, laid out as published, from the repository's copies."""
    shutil.copytree(CLEAN_DIR, tmp_path / LESSON_PLANS / "notes")
    (tmp_path / RATINGS / "inputs").mkdir(parents=True)
    shutil.copy(EVAL_SET_PATH, tmp_path / RATINGS / "inputs" / "eval_set.json")
    _provenance(tmp_path / LESSON_PLANS)
    _provenance(tmp_path / RATINGS)
    return tmp_path


def _assert_reproduces_part_1(lessons: list[StudyLesson]) -> None:
    part_1 = part_1_inputs()
    assert sorted(lesson.lesson for lesson in lessons) == sorted(part_1)
    for lesson in lessons:
        rebuilt = with_lesson_note(lesson.plan, dict(lesson.note_sections))
        for condition in CONDITIONS:
            assert part_1_request(rebuilt, condition) == part_1_request(
                part_1[lesson.lesson], condition
            ), f"{lesson.lesson} {condition.value}"
    notes = "".join(sorted(body for lesson in lessons for _, body in lesson.note_sections))
    recorded = json.loads((PART_1 / "fingerprint.json").read_text())["inputs"]["notes.clean"]
    assert hashlib.sha256(notes.encode()).hexdigest()[:12] == recorded


def test_part_1_used_the_settings_this_test_reproduces() -> None:
    assert (RUN["note_source"], RUN["figures"], RUN["context_variant"]) == (
        "clean",
        "source",
        "v7-full",
    )


def test_an_imported_lesson_rebuilds_part_1s_input(repo_release: Path) -> None:
    _assert_reproduces_part_1(ReleasedStudy(repo_release).lessons())


def test_a_file_that_differs_from_its_record_is_refused(repo_release: Path) -> None:
    note = next((repo_release / LESSON_PLANS / "notes").rglob("*.md"))
    note.write_text(note.read_text() + " ")

    with pytest.raises(DatasetMismatchError, match="differs from its PROVENANCE.json"):
        ReleasedStudy(repo_release).lessons()


@pytest.mark.skipif(
    not (RELEASE / LESSON_PLANS).is_dir(), reason="the published datasets are not here"
)
def test_the_published_study_rebuilds_part_1s_input() -> None:
    _assert_reproduces_part_1(ReleasedStudy(RELEASE).lessons())
