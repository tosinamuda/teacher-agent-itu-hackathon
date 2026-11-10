"""Read a built set the way a rater will: on the page, not in the markdown.

Whether a document is followable is a fact about its pages — where a section starts,
whether a scoring page holds everything needed to score, whether anything a rater must
act on is stranded at the foot of a sheet. None of that is visible in the markdown, so
this converts each document to PDF and checks the shape that carries the rater through:

    uv run python -m experiments.human_rating.inspect

Needs LibreOffice to convert and poppler's ``pdftotext`` to read. Both are developer
tools, not part of the build a rater's documents come from.
"""

from __future__ import annotations

import argparse
import re
import shutil
import statistics
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from .__main__ import latest_build

SOFFICE = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
OBJECTIVE = re.compile(r"^Objective (\d+) of (\d+) — .+$", re.M)
#: Every page title. A page without one is a continuation of the page before it.
TITLE = re.compile(
    r"^(?:The lesson|Objective \d+ of \d+ — .+|The complete Material .+|Closing comments)\s*$",
    re.M,
)
FOOTER = re.compile(r"Rater \d+ \| Evaluation Set \S+.*Page \d+ of \d+", re.S)
SCORING = "— your scores"


def soffice() -> Path:
    found = SOFFICE if SOFFICE.exists() else shutil.which("soffice")
    if not found:
        raise SystemExit("LibreOffice not found: install it, or pass --pdfs with converted files")
    return Path(found)


def to_pdfs(documents: list[Path], out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    # A profile of its own: a LibreOffice already open on the user's profile takes the job and
    # converts nothing.
    profile = (out / ".soffice-profile").resolve().as_uri()
    subprocess.run(
        [
            str(soffice()),
            f"-env:UserInstallation={profile}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out),
            *map(str, documents),
        ],
        check=True,
        capture_output=True,
    )
    return sorted(out.glob("*.pdf"))


def pages(pdf: Path) -> list[str]:
    text = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True, text=True
    ).stdout
    return text.split("\f")[:-1]


def problems(pdf: Path) -> list[str]:
    """Everything about this document that would make a rater lose their place."""
    sheets = pages(pdf)
    found: list[str] = []
    if len(sheets) < 3:
        return [f"{pdf.name}: {len(sheets)} pages"]
    if "Lesson reference" not in sheets[0] or "What to do." in sheets[0]:
        found.append(f"{pdf.name}: the cover is not a page of its own")
    if not sheets[1].lstrip().startswith("Instructions"):
        found.append(f"{pdf.name}: the instructions are not page 2")
    if not sheets[2].lstrip().startswith("The lesson"):
        found.append(f"{pdf.name}: the lesson is not page 3")
    seen = []
    for index, sheet in enumerate(sheets[2:], start=3):
        top = sheet.index(sheet.lstrip())
        for match in TITLE.finditer(sheet):
            if match.start() != top:
                found.append(f"{pdf.name} p{index}: {match.group(0)[:40]!r} starts mid-page")
        for match in OBJECTIVE.finditer(sheet):
            seen.append(int(match.group(1)))
        if SCORING in sheet and "What each score means" not in sheet:
            found.append(f"{pdf.name} p{index}: a scoring page without the criteria")
    for index, sheet in enumerate(sheets, start=1):
        if not FOOTER.search(sheet):
            found.append(f"{pdf.name} p{index}: no footer")
    if seen != sorted(seen):
        found.append(f"{pdf.name}: objective pages run {seen}")
    expected = int(OBJECTIVE.search(sheets[3]).group(2)) if OBJECTIVE.search(sheets[3]) else 0
    if expected and sorted(set(seen)) != list(range(1, expected + 1)):
        found.append(f"{pdf.name}: objectives {sorted(set(seen))} of {expected}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sets", type=Path, default=None, help="defaults to the latest build")
    parser.add_argument("--pdfs", type=Path, help="where to keep the conversions")
    args = parser.parse_args()
    sets = args.sets or latest_build()
    if sets is None:
        raise SystemExit("no build to inspect: run experiments.human_rating first")
    documents = sorted(p for p in sets.glob("Rater-*/**/*.docx") if "-P" in p.name)
    if not documents:
        raise SystemExit(f"no evaluation sets under {sets}")
    directory = args.pdfs or Path(tempfile.mkdtemp(prefix="human-rating-"))
    pdfs = to_pdfs(documents, directory)
    counts: dict[str, list[int]] = defaultdict(list)
    found: list[str] = []
    for pdf in pdfs:
        counts["Part 1" if "-P1-" in pdf.name else "Part 2"].append(len(pages(pdf)))
        found += problems(pdf)
    for part, lengths in sorted(counts.items()):
        print(
            f"  {part}: {len(lengths)} sets, "
            f"{min(lengths)}–{max(lengths)} pages (median {statistics.median(lengths):g}), "
            f"{sum(lengths)} in all"
        )
    print(f"  {len(found)} structural problems")
    print("\n".join(found[:40]))
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
