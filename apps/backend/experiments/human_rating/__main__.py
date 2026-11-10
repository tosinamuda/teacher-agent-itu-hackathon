"""Build every rater's folder of Evaluation Sets, and the researcher's key beside them.

    uv run python -m experiments.human_rating --h2-run h2-deepseek-52 \\
        --h2-runs-dir /path/to/h2_personalisation_eval/runs

One folder per rater, one .docx per assignment in the workbook's delivery order, a
general-instructions document first. The `_key` folder maps every external id back to
the condition, draw, learner and A/B order, and is the one thing here that must not be
shared with a rater. The whole output directory is ignored by git: Part 2 embeds
learners' classwork.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from . import h1_document, h2_comparative, mapping, render, sources
from .instructions import general_instructions_markdown

HERE = Path(__file__).resolve().parent
#: Each build writes a folder of its own, stamped with the minute it started, so a
#: rebuild never overwrites one that has been sent to a rater. The published copy is
#: archived separately under ``delivered/``.
BUILDS = HERE / "builds"
DEFAULT_H1_RUN = "c0c3-prism-objective"


def _name(part: int, order: int, external_id: str) -> str:
    return f"R{{}}-P{part}-{order:02d} {external_id}.docx"


def latest_build(builds: Path = BUILDS) -> Path | None:
    """The most recent build, which is what a check without arguments should read."""
    folders = sorted(p for p in builds.glob("*") if p.is_dir())
    return folders[-1] if folders else None


def _provenance(out: Path, h1: sources.H1Run, h2: sources.H2Run, started: str) -> None:
    """What this build was made from, beside the documents it made."""
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=HERE
    ).stdout.strip()
    (out / "build.json").write_text(
        json.dumps(
            {
                "built": started,
                "commit": revision or None,
                "h1_run": h1.label,
                "h1_arm": h1.arm,
                "h2_run": h2.label,
                "h2_model": h2.model,
                "h2_base": h2.base,
            },
            indent=2,
        )
        + "\n"
    )


def build(args: argparse.Namespace) -> int:
    started = datetime.now(UTC).strftime("%Y-%m-%dT%H%M%SZ")
    if args.out is None:
        args.out = BUILDS / started
    plans = sources.plans()
    h1_run = sources.H1Run(args.h1_run, args.h1_runs_dir)
    h2_run = sources.H2Run(args.h2_run, args.h2_runs_dir)
    h1 = mapping.load_h1()
    h2 = mapping.load_h2()
    _check_h2_coverage(h2, h2_run)

    key: dict[str, list[dict]] = {"h1": [], "h2": []}
    sensitive: Counter[str] = Counter()
    panels: Counter[str] = Counter()
    for rater in mapping.RATERS:
        number = int(rater.split("-")[1])
        folder = args.out / f"Rater-{number}"
        render.to_docx(
            general_instructions_markdown(number),
            folder / f"R{number}-00 General instructions.docx",
            rater_number=number,
            set_id="General instructions",
        )
        for a in (x for x in h1 if x.rater == rater):
            plan = plans[a.lesson]
            text = h1_document.markdown(a, plan, h1_run.pack(a.lesson, a.condition, a.version))
            path = (
                folder
                / "Part 1 - Class revision material"
                / _name(1, a.order, a.external_id).format(number)
            )
            render.to_docx(
                text, path, rater_number=number, set_id=f"Evaluation Set {a.external_id}"
            )
            sensitive.update(render.sensitive_words(text))
            panels[rater] += len(plan["lesson_plan_objectives"])
            key["h1"].append({**a.__dict__, "run": h1_run.label, "sha256": _sha(path)})
        for a in (x for x in h2 if x.rater == rater):
            plan = plans[a.lesson]
            materials = h2_run.materials(a.lesson, a.student)
            evidence = sources.learner_evidence(a.lesson, a.student)
            text = h2_comparative.markdown(a, plan, materials, evidence)
            path = (
                folder
                / "Part 2 - Student-specific revision material"
                / _name(2, a.order, a.external_id).format(number)
            )
            render.to_docx(
                text, path, rater_number=number, set_id=f"Evaluation Set {a.external_id}"
            )
            sensitive.update(render.sensitive_words(text))
            panels[f"{rater} h2"] += len(evidence)
            key["h2"].append(
                {
                    **a.__dict__,
                    "run": h2_run.label,
                    "base": h2_run.base,
                    "rated_objectives": [e.objective_id for e in evidence],
                    # Not on any page a rater reads: it is the instruction the adapted
                    # material was written from, so it is kept for the analysis only.
                    "bands": {e.objective_id: e.band for e in evidence},
                    "sha256": _sha(path),
                }
            )
    key_dir = args.out / "_key"
    key_dir.mkdir(parents=True, exist_ok=True)
    (key_dir / "key.json").write_text(json.dumps(key, indent=2) + "\n")
    _provenance(args.out, h1_run, h2_run, started)
    _report(h1, h2, panels, sensitive, args.out)
    return 0


def _check_h2_coverage(h2: list[mapping.H2Assignment], run: sources.H2Run) -> None:
    wanted = {(a.lesson, a.student) for a in h2}
    missing = wanted - run.learners()
    if missing:
        raise SystemExit(f"{run.label} has no P0/P1 for {sorted(missing)}")


def _report(h1, h2, panels: Counter, sensitive: Counter, out: Path) -> None:
    """Sets built against the workbook's own printed-row count; panels are reported.

    The workbook states how many sets each rater is printed, not how many objective
    panels those sets carry, so the panel counts are shown rather than checked here —
    every set's panels are checked against its own lesson as it is written.
    """
    expected_h1 = mapping.expected_checks(mapping.H1_WORKBOOK)["printed rows"]
    expected_h2 = mapping.expected_checks(mapping.H2_WORKBOOK)["printed rows"]
    print(f"  {out}")
    print(
        f"  {'rater':9s} {'part 1 sets':>12s} {'expected':>9s} {'panels':>8s} | "
        f"{'part 2 sets':>12s} {'expected':>9s} {'panels':>8s}"
    )
    for rater in mapping.RATERS:
        n1 = sum(1 for a in h1 if a.rater == rater)
        n2 = sum(1 for a in h2 if a.rater == rater)
        e1, e2 = expected_h1[rater], expected_h2[rater]
        flag1 = "" if str(n1) == e1 else "  <- MISMATCH"
        flag2 = "" if str(n2) == e2 else "  <- MISMATCH"
        print(
            f"  {rater:9s} {n1:>12d} {e1:>9s} {panels[rater]:>8d}{flag1} | "
            f"{n2:>12d} {e2:>9s} {panels[f'{rater} h2']:>8d}{flag2}"
        )
    if sensitive:
        print(f"  words to review by eye: {dict(sensitive)}")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--h1-run", default=DEFAULT_H1_RUN)
    parser.add_argument("--h1-runs-dir", type=Path, default=sources.H1_RUNS)
    parser.add_argument("--h2-run", required=True, help="the personalisation run holding P0 and P1")
    parser.add_argument("--h2-runs-dir", type=Path, default=sources.H2_RUNS)
    parser.add_argument(
        "--out", type=Path, default=None, help="defaults to a new timestamped build folder"
    )
    return build(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
