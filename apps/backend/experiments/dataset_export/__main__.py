"""Build, verify and upload the four LPCG datasets.

    uv run python -m experiments.dataset_export build [--out DIR] [--replace]
    uv run python -m experiments.dataset_export verify [--out DIR]
    uv run python -m experiments.dataset_export upload [--out DIR]

The four are always built and verified together: a digest published in one of them can give
back what another rewrote. A build is always verified, and an upload re-verifies what is on
disk against the sources first; it sends nothing unless every dataset is clean and carries its
card, and it creates every repository private.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .build import Release, collect, write
from .cards import missing_tables, write_cards
from .indexes import indexed
from .seal import seal
from .sources import datasets
from .upload import upload
from .verify import Report, against, leaks, verify

#: Beside the private study record, under the one study-data folder.
DEFAULT_OUT = Path.home() / "Documents/Unilag/Masters/Thesis/Dataset/public"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("command", choices=("build", "verify", "upload"))
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args(argv)

    collected = [collect(dataset) for dataset in datasets()]
    replaced = seal(collected)
    releases = [indexed(release) for release in collected]
    if args.command == "build":
        for release in releases:
            root = write(release, args.out, replace=args.replace)
            write_cards(release, root, len(replaced))
            print(f"built {release.name} -> {root}")
    print(f"{len(replaced)} digest(s) of an original replaced with the published form's")
    if _problems(args.out, releases):
        return 1
    if args.command == "upload":
        uploaded, collection = upload(args.out / release.name for release in releases)
        for item in uploaded:
            print(f"  {item.repo_id} at {item.commit[:12]}: {item.url}")
        print(f"  collection: {collection}")
    return 0


def _problems(out: Path, releases: list[Release]) -> int:
    reports = [verify(out / release.name) for release in releases]
    for report, release in zip(reports, releases, strict=True):
        report.problems.extend(against(release, out / release.name))
        if not (out / release.name / "README.md").exists():
            report.problems.append("README.md: the dataset has no card")
        else:
            report.problems.extend(
                f"README.md: the viewer reads {path}, which the dataset does not hold"
                for path in missing_tables(out / release.name)
            )
        _print(report)
    across = leaks(reports, releases)
    print(f"  across datasets: {f'{len(across)} problem(s)' if across else 'clean'}")
    for problem in across[:25]:
        print(f"    {problem}")
    return len(across) + sum(len(report.problems) for report in reports)


def _print(report: Report) -> None:
    status = "clean" if not report.problems else f"{len(report.problems)} problem(s)"
    unread = ", ".join(f"{count} {suffix}" for suffix, count in sorted(report.unread.items()))
    line = f"  {report.dataset}: {report.files} files, {status}"
    print(f"{line}; not text-read: {unread}" if unread else line)
    for problem in report.problems[:25]:
        print(f"    {problem}")


if __name__ == "__main__":
    raise SystemExit(main())
