"""What goes into each of the four datasets, and where it comes from.

A dataset is a list of sources. Each source names a repository, the revision to read, a
path inside it, where that path lands in the published tree, and which files under it are
left out. Files are read from git objects at the named revision, never from a working
tree: an uncommitted edit cannot reach a release, and neither can an ignored scratch file
sitting beside the runs.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path


@dataclass(frozen=True)
class Repository:
    name: str
    root: Path


CODE = Repository("lpcg", Path(__file__).resolve().parents[4])
STUDY = Repository(
    "thesis-dataset", Path.home() / "Documents/Unilag/Masters/Thesis/Dataset/private/study-record"
)

#: The study as reported. Every run fingerprint in the corpus was recorded against it.
STUDY_TAG = "msc-study-2026-09"

PROCESSED = "dataset/processed"
H1 = "apps/backend/experiments/h1_condition_eval"
H2 = "apps/backend/experiments/h2_personalisation_eval"
RATING = "apps/backend/experiments/human_rating"

#: The prototype is seeded from this folder's top-level rows; the review audit and triage
#: that account for each row's status sit beside them and ship with them.
LINKAGE = f"{PROCESSED}/ao_textbook_linkage/manual"

#: The study record kept outside the code repository. Its workbook is the only one released:
#: the snapshot committed beside the rating code was taken before rating closed. Results are
#: reported in the dissertation, so no analysis output is released.
STUDY_RECORD = "experiments"
COMPLETE_RATINGS = "2026-09-13-ratings.xlsx"
RATER_GUIDE = "Research_Assistant_Guide_Mathematics_Revision_Evaluation.docx"
PILOT_SHEETS = "t3-w05-rater-worksheets-C0-C3.pdf"

#: Each puts the original photograph beside its transcription, to check one against the
#: other. They are the only photographs in any source; every other render is typeset.
PHOTOGRAPHS = frozenset({"_render/comparison-figures.png", "_render/comparison-student-01.png"})


def _everything(relative: str) -> bool:
    return True


@dataclass(frozen=True)
class Source:
    repo: Repository
    revision: str
    path: str
    lands: str
    keep: Callable[[str], bool] = field(default=_everything)


@dataclass(frozen=True)
class Dataset:
    name: str
    sources: tuple[Source, ...]


def datasets() -> tuple[Dataset, ...]:
    code = partial(Source, CODE, STUDY_TAG)
    study = partial(Source, STUDY, "HEAD")
    return (
        Dataset(
            "ng-jss1-math-curriculum",
            (
                code(f"{PROCESSED}/curriculum", "curriculum"),
                code(f"{PROCESSED}/scheme-of-work", "scheme-of-work"),
            ),
        ),
        Dataset(
            "ng-jss1-math-textbook-linkage",
            (
                code(f"{PROCESSED}/textbook", "textbook"),
                code(LINKAGE, "linkage"),
            ),
        ),
        Dataset(
            "ng-jss1-math-lesson-plans",
            (
                code(f"{H1}/lessons", "lessons"),
                code(f"{H1}/notes-clean", "notes"),
                code(f"{H1}/student_work.json", "coding/student_work.json"),
                code(f"{H1}/note_headings.json", "coding/note_headings.json"),
                code(f"{H1}/selection_set.json", "coding/selection_set.json"),
                study("transcripts", "transcripts", keep=lambda rel: rel not in PHOTOGRAPHS),
            ),
        ),
        Dataset(
            "ng-jss1-math-alignment-ratings",
            (
                code(f"{H1}/eval_set.json", "inputs/eval_set.json"),
                code(f"{H1}/frozen", "inputs/frozen"),
                code(f"{H1}/runs", "runs/h1"),
                code(f"{H1}/wire", "runs/h1-wire"),
                code(f"{H2}/runs", "runs/h2"),
                code(f"{RATING}/delivered", "ratings/delivered"),
                code(f"{RATING}/mapping", "ratings/allocation"),
                study(
                    f"{STUDY_RECORD}/{COMPLETE_RATINGS}", f"ratings/workbooks/{COMPLETE_RATINGS}"
                ),
                study(f"{STUDY_RECORD}/{RATER_GUIDE}", f"ratings/instrument/{RATER_GUIDE}"),
                study(f"{STUDY_RECORD}/{PILOT_SHEETS}", f"ratings/instrument/pilot/{PILOT_SHEETS}"),
            ),
        ),
    )
