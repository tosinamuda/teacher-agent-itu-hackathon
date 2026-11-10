"""Assemble the whole Part 2 handoff bundle from one command.

The tables come from :mod:`export` and the reconciliation from :mod:`validation`; this
adds the three documents an analyst needs to read the tables correctly, hashes every
file, and zips the result. It exists as its own module because an export that has to be
finished by hand is an export nobody can reproduce — the first version of this bundle was
assembled from ad-hoc scripts and could not be rebuilt after the directory was cleared.

The rubric document is generated from ``protocol.py``, the module that rendered the rater
documents, so it cannot drift from what the raters actually saw.

Run with::

    uv run python -m experiments.human_rating.handoff "<delivered folder>" <out dir>
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from app.domains.evaluation.domain.study_instrument import COMPARISON, H2_CRITERIA

from . import export, provenance, sources, validation

#: Every estimate reported to the researcher from this dataset, with the metadata that
#: says what it measured. Withdrawn ones stay: a reader checking the analysis needs to
#: know which numbers were retracted and why, and that is not recoverable from the code.
REPORTED = Path(__file__).resolve().parent / "reported_results.csv"


def _score_row(option: str) -> tuple[int, int]:
    """The five-point and collapsed scores for one option, read as if B were P1."""
    if "same" in option.lower():
        return 0, 0
    size = 2 if "clearly" in option.lower() else 1
    sign = 1 if option.startswith("B") else -1
    return size * sign, sign


def rubric_markdown() -> str:
    """What a rater saw and how it becomes a number, from the module that rendered it."""
    lines = [
        "# Part 2 rubric and design",
        "",
        "Generated from `app/domains/evaluation/domain/study_instrument.py`, the module that",
        "rendered the rater documents, so it cannot drift from what raters actually saw. Design",
        "facts that live outside that module are recorded below and marked where nothing was",
        "written down.",
        "",
        "## What a rater saw",
        "",
        "One document per assigned comparison: a cover page; instructions; the lesson reference;",
        "then per objective (a) what the teacher taught, (b) the learner's marked class work,",
        "(c) the two materials side by side, (d) the comparison table. Both materials are",
        "reprinted in full at the end. Raters were blind to condition and the A/B labels carry",
        "no meaning across documents.",
        "",
        "## Response options",
        "",
        "Five options, one tick per row. The rater writes only a mark (`Yes`, `yes` or a check",
        "glyph); **the response is which column carries it**, not the text typed.",
        "",
        "| option | five-point | collapsed |",
        "| --- | ---: | ---: |",
    ]
    for option in COMPARISON:
        five, three = _score_row(option)
        lines.append(f"| {option} | {five:+d} | {three:+d} |")
    lines += [
        "",
        "Scores above assume the option's side is P1. **`condition_a`/`condition_b` in",
        "`ratings_long.csv` give the mapping for that row**; when the side is P0 the sign flips.",
        "Positive always means the personalised material was preferred. `score_coding_id =",
        f"{export.SCORE_CODING}` names the five-point column.",
        "",
        "A/B order is **opposite between the two copies of every case**, so position is",
        "counterbalanced within panel rather than across the study.",
        "",
        "## The three criteria, as the rater saw them",
        "",
    ]
    for index, criterion in enumerate(H2_CRITERIA, 1):
        lines += [
            f"### {index}. {criterion.construct} (`{criterion.id}`)",
            "",
            f"**Row label:** {criterion.name}",
            "",
            f"**Question:** {criterion.question}",
            "",
            f'**"Better" anchor:** {criterion.better}',
            "",
        ]
        if criterion.notes:
            lines += ["**Notes given to raters:**", *[f"- {n}" for n in criterion.notes], ""]
    lines += [
        "## Assignment and blinding",
        "",
        "- 26 learner-lesson cases, each delivered **twice** with different blind packet ids",
        "  and opposite A/B order; 52 assignments over 4 raters, 13 each.",
        "- Every case is rated by exactly two raters and all six rater pairs are connected",
        "  (R1-R2 5, R1-R3 4, R1-R4 4, R2-R3 4, R2-R4 4, R3-R4 5).",
        "- The internal packet id carries a copy suffix (`h2-l01-s02-c1` / `-c2`). **Strip the",
        "  trailing `-c<n>` to recover the case.** `panel_id` is already case-level and is the",
        "  correct join key.",
        "",
        "## Rated objectives",
        "",
        "Not every objective carries a panel — only those the student has class work for, sorted",
        "into curriculum order. Documents hold one or two panels; 35 distinct panels across 26",
        "cases. **The panel's ordinal therefore does not identify its objective**; the heading",
        "does, and `objective_resolved_from` records that it was read from there.",
        "",
        "## Missingness",
        "",
        "An unanswered row is `response_status = blank` with an empty `score_used`. **It is",
        "never scored 0.** Zero is reserved for an actual `About the same`. No reason was",
        "recorded for any blank.",
        "",
        "## Aggregation is not prescribed here",
        "",
        "`validation_report.md` shows one route (unweighted mean of a learner's answered cells)",
        "and states what it weights. Averaging criteria within objective, then objectives within",
        "lesson, then lessons, gives different weights under unequal completion. The analyst",
        "should choose the target average explicitly: sampled learner, learner-lesson case, or",
        "criterion judgement.",
        "",
        "## What was specified when",
        "",
        "- The comparative instrument was published 2026-09-04; all ratings used it",
        "  (`rubric_version = h2_comparative_2026-09-04`).",
        "- The pre-registration (frozen 2026-07-26) covers",
        "  **H1** and names C1 vs C0 as the central comparison. It does **not** specify any",
        "  Part 2 attainment-stratum analysis.",
        "- **The attainment-stratum contrast was chosen after seeing the ratings.** It is",
        "  exploratory and should be labelled as such wherever it is reported.",
        "",
        "## Comparator provenance",
        "",
        "P0 is **not** an objectives-only baseline. It is the C3 artefact from run",
        "`c0c3-prism-objective`, condition `C3`, repeat 1 — the fully configured class-level",
        "pipeline including scoped retrieval and the validation/repair rung. Part 2 measures the",
        "**increment** of the learner model over that configuration, not the framework itself.",
        "",
        "One P0 pack per lesson is reused across every learner in that lesson (3 packs, 26",
        "cases). P1 is distinct per learner and differs from P0 in all 26.",
        "",
    ]
    return "\n".join(lines)


README = """# Part 2 analysis handoff

Snapshot of the Part 2 (H2) human comparative evaluation for independent analysis.
Nothing here is a fitted conclusion.

Rebuild with::

    uv run python -m experiments.human_rating.handoff "<delivered folder>" <out dir>

## Read in this order

1. `reproduction/validation_report.md` — every count recomputed from the exported table
2. `part2/rubric_and_design.md` — what a rater saw, the response coding, the A/B rule
3. `reproduction/reported_results.csv` — every previously reported estimate with its
   method, unit, weighting and status. **Seven of eleven are withdrawn, not defended, or
   flagged as misleading as stated.**
4. `part2/panel_provenance.csv` — what each of the 70 rater-panels actually displayed
5. `part2/objective_generation_audit.csv` — per objective: learner state, whether it was
   shown, and whether P1 changed that objective's sections
6. `part2/ratings_long.csv` — the data

## Four things that will bite an analyst who skips the above

**Join on `panel_id`, never on a packet id.** Each case was delivered twice, with
different blind packet ids and opposite A/B order. The internal id carries a copy suffix
(`h2-l01-s02-c1` / `-c2`); joining on it treats two independent ratings of the same
material as two different targets. That exact error was made here and produced a claim
that the design had no rater overlap, when in fact every panel is doubly rated.

**A panel's objective is the one its heading names, never the one at its position.** Only
objectives a student has class work for get a panel, so the shown objectives are a subset
of the lesson's list, not a prefix. Reading the ordinal misidentified 36 of 70 panels here
and manufactured an entire reported finding — see `panel_provenance.csv`, which keeps the
old value beside the right one.

**The 26 cases are not independent.** Nine learners recur across three lessons, and one
P0 pack per lesson is shared by every learner in it — three base packs behind 26 cases.

**P0 is the C3 artefact, not an objectives-only baseline.** Part 2 measures the increment
of the learner model over the fully configured class-level pipeline.

## Deliberately absent

- **Pack text and learner class work** — real minors' work, held back pending an explicit
  sharing decision. `cases.csv` carries SHA-256 content hashes, so reuse and difference
  are verifiable without the text.
- **A chosen primary test.** Existing analyses are exported for verification; the
  permutation test is a candidate, not a declaration.

## Known unknowns

No per-cell timestamps (Google Docs exposes none). No recorded reason for any of the 11
blanks. The sampling strata were never recorded and are reconstructed post hoc — from the
same class work that produced the P1 learner state. Rater-4 has not finished.
"""


#: The libraries every reported estimate passed through. Pinned by reading the running
#: interpreter rather than the lockfile, so the file records what actually computed them.
_ANALYSIS_LIBRARIES = ("numpy", "openpyxl", "pandas", "scipy", "statsmodels")


def _versions() -> str:
    from importlib.metadata import PackageNotFoundError, version

    lines = [f"python=={sys.version.split()[0]}"]
    for name in _ANALYSIS_LIBRARIES:
        try:
            lines.append(f"{name}=={version(name)}")
        except PackageNotFoundError:
            lines.append(f"# {name}: not installed")
    return "\n".join(lines) + "\n"


def _hashes(out: Path) -> dict[str, Any]:
    return {
        str(path.relative_to(out)): {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
        for path in sorted(out.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def _structural_facts(run: str) -> dict[str, Any]:
    record = json.loads((sources.H2_RUNS / run / "run.json").read_text())
    packs = export.artefacts(run)
    outcomes = [v for pack in packs.values() for v in pack.evidence.values()]
    return {
        "p0_is": f"the {record['base']['condition']} artefact from run "
        f"{record['base']['run']}, repeat {record['base']['repeat']}",
        "p0_packs_distinct": len({p.p0_hash for p in packs.values()}),
        "p0_packs_reused_across_cases": len(packs),
        "p1_identical_to_p0_in_cases": sum(1 for p in packs.values() if p.p0_hash == p.p1_hash),
        "objective_rows_with_learner_state": outcomes.count("personalised"),
        "objective_rows_without_learner_state": outcomes.count("no_learner_state"),
        "copy_suffix_warning": "internal_packet_id ends in -c1/-c2; strip it to get the case",
        "join_key": "panel_id",
    }


def build(folder: Path, out: Path, run: str = export.RUN) -> Path:
    plans = sources.plans()
    export.bundle(folder, out)
    export.write_csv(
        out / "part2" / "panel_provenance.csv", provenance.panel_provenance(folder, plans)
    )
    export.write_csv(
        out / "part2" / "objective_generation_audit.csv",
        provenance.objective_generation_audit(folder, plans, run),
    )
    (out / "part2" / "rubric_and_design.md").write_text(rubric_markdown(), encoding="utf-8")
    (out / "README.md").write_text(README, encoding="utf-8")

    repro = out / "reproduction"
    repro.mkdir(parents=True, exist_ok=True)
    (repro / "validation_report.md").write_text(validation.report(out), encoding="utf-8")
    shutil.copy(REPORTED, repro / "reported_results.csv")
    here = Path(__file__).resolve().parent
    scripts = repro / "scripts"
    scripts.mkdir(exist_ok=True)
    for name in ("export.py", "validation.py", "handoff.py"):
        shutil.copy(here / name, scripts / name)
    shutil.copytree(here / "analysis_as_run", repro / "analysis_as_run", dirs_exist_ok=True)
    (repro / "requirements.txt").write_text(_versions(), encoding="utf-8")

    exports = out / "source_exports"
    exports.mkdir(exist_ok=True)
    shutil.copy(
        Path(__file__).resolve().parent / "mapping" / "h2.xlsx",
        exports / "h2_assignment_mapping.xlsx",
    )

    manifest = json.loads((out / "manifest.json").read_text())
    manifest["structural_facts"] = _structural_facts(run)
    manifest["files"] = _hashes(out)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return shutil.make_archive(str(out.parent / f"{out.name}"), "zip", out.parent, out.name)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    print(f"wrote {build(Path(sys.argv[1]), Path(sys.argv[2]))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
