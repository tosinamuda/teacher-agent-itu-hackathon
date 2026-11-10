"""Report verbatim word runs shared between paper.pdf and a directory of sources.

Turnitin's value is its corpus, not its matching. This does the matching part over a
corpus you supply: point it at the PDFs of the work the paper draws on and it prints
every run of N or more consecutive words that appears in both.

    python check_overlap.py <sources-dir> [N]
"""

import pathlib
import re
import subprocess
import sys

STOP_AT = "References"


def words(text: str) -> list[str]:
    text = re.sub(r"\[[^\]]*\]", " ", text)
    return re.sub(r"[^A-Za-z0-9' ]", " ", text.lower()).split()


def text_of(pdf: pathlib.Path) -> str:
    return subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout


def is_prose(run: str) -> bool:
    """Drop page furniture — numbering, headers, the venue's own footer."""
    parts = run.split()
    return sum(part.isalpha() for part in parts) >= 0.7 * len(parts)


def shared_runs(body: list[str], source: list[str], n: int) -> list[str]:
    seen = {tuple(source[i : i + n]) for i in range(len(source) - n + 1)}
    runs, i = [], 0
    while i <= len(body) - n:
        if tuple(body[i : i + n]) not in seen:
            i += 1
            continue
        end = i
        while end <= len(body) - n and tuple(body[end : end + n]) in seen:
            end += 1
        run = " ".join(body[i : end + n - 1])
        if is_prose(run):
            runs.append(run)
        i = end
    return runs


def main() -> None:
    sources = pathlib.Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    body = words(text_of(pathlib.Path("paper.pdf")).split(STOP_AT)[0])
    total = 0
    for pdf in sorted(sources.glob("*.pdf")):
        runs = shared_runs(body, words(text_of(pdf)), n)
        shared = sum(len(run.split()) for run in runs)
        total += shared
        print(f"{pdf.stem:24} {len(runs):3} runs {shared:5} words {100 * shared / len(body):6.2f}%")
        for run in runs:
            print(f"    {len(run.split())}w | {run[:140]}")
    print(f"{'TOTAL':24} {total} of {len(body)} words = {100 * total / len(body):.2f}%")


if __name__ == "__main__":
    main()
