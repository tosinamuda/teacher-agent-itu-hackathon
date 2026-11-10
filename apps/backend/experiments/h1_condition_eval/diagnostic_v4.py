"""Read the v4 diagnostic exactly as DIAGNOSTIC-V4.md predeclared it.

Three arms from two runs — D0 and D1 from `diag-v3`, D2 from `diag-v4` — each
judged twice. Every number here was named before any output existed: the
endpoint, the margin, the overlap check, and the triggers. The script reports
them and nothing it found afterwards.

    uv run python -m experiments.h1_condition_eval.diagnostic_v4
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

from scipy.stats import spearmanr

from app.domains.evaluation.application.statistics import wilcoxon_p

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
OUT = RUNS / "DIAGNOSTIC-V4-RESULTS.md"

ARMS = {"D0": ("diag-v3", "C0"), "D1": ("diag-v3", "C1"), "D2": ("diag-v4", "C1")}
ABLATION = {"D3": ("diag-v4-noassess", "C1")}
#: The v7-full contrast: C0 and the frozen C1 from one run, the fully represented
#: C1 from another. C0 is generated once — identical across the variants on the
#: wire — so both C1 arms pair against the same baseline.
FULL_ARMS = {"E0": ("full-v3", "C0"), "E1": ("full-v3", "C1"), "E2": ("full-v7", "C1")}
FULL_NULL_BAND = 0.25
FULL_EFFECT = 0.5
ABLATION_NULL_BAND = 0.25
ABLATION_EFFECT = -0.5
DIMENSIONS = (
    "taught_lesson_alignment",
    "objective_curriculum_alignment",
    "scope_conceptual_correctness",
    "clarity_usefulness",
)
ENDPOINT = "taught_lesson_alignment"
NON_INFERIORITY_MARGIN = 0.5
OVERLAP_TRIGGER = 0.5
PASSES = ("a", "b")

Cell = dict[str, dict[str, list[float]]]  # lesson -> dimension -> draws


def _load(run: str, condition: str, judge_pass: str) -> tuple[Cell, dict[str, dict]]:
    rating = RUNS / run / "rating"
    key = {r["candidate_id"]: r for r in json.loads((rating / "_key.json").read_text())}
    data = json.loads((rating / f"judgments_pass_{judge_pass}.json").read_text())
    cell: Cell = {}
    overlap: dict[str, dict] = {}
    for j in data["judgments"]:
        row = key[j["candidate_id"]]
        if row["condition"] != condition:
            continue
        for dim in DIMENSIONS:
            cell.setdefault(row["lesson"], {}).setdefault(dim, []).append(float(j[dim]["score"]))
        overlap[j["candidate_id"]] = {
            "lesson": row["lesson"],
            "reuse": row["evaluation_overlap"]["reused_normalised"],
            "score": float(j[ENDPOINT]["score"]),
        }
    return cell, overlap


def _lesson_means(cell: Cell, dim: str) -> dict[str, float]:
    return {lesson: statistics.fmean(dims[dim]) for lesson, dims in cell.items()}


def _paired(a: dict[str, float], b: dict[str, float]) -> tuple[list[float], list[float], list[str]]:
    lessons = sorted(set(a) & set(b))
    return [a[x] for x in lessons], [b[x] for x in lessons], lessons


def _contrast(treat: Cell, base: Cell, dim: str) -> dict:
    t, b, lessons = _paired(_lesson_means(treat, dim), _lesson_means(base, dim))
    diffs = [x - y for x, y in zip(t, b, strict=True)]
    return {
        "lessons": lessons,
        "diffs": diffs,
        "mean": statistics.fmean(diffs),
        "signs": (sum(d > 0 for d in diffs), sum(d == 0 for d in diffs), sum(d < 0 for d in diffs)),
        "p": wilcoxon_p(t, b),
    }


def _fmt_contrast(name: str, c: dict) -> str:
    pos, zero, neg = c["signs"]
    p = "—" if c["p"] is None else f"{c['p']:.3f}"
    per = ", ".join(f"{x} {d:+.2f}" for x, d in zip(c["lessons"], c["diffs"], strict=True))
    return f"| {name} | {c['mean']:+.2f} | {pos}/{zero}/{neg} | {p} | {per} |"


def _overlap_rho(overlap: dict[str, dict]) -> tuple[float | None, int]:
    rows = list(overlap.values())
    xs = [r["reuse"] for r in rows]
    ys = [r["score"] for r in rows]
    if len(set(xs)) < 2 or len(set(ys)) < 2:
        return None, len(rows)
    rho = spearmanr(xs, ys).statistic
    return float(rho), len(rows)


def _pool(cells: list[Cell]) -> Cell:
    """Repeated judgments of the same candidate averaged before the lesson mean."""
    pooled: Cell = {}
    for lesson in cells[0]:
        for dim in DIMENSIONS:
            draws = list(zip(*(c[lesson][dim] for c in cells), strict=True))
            pooled.setdefault(lesson, {})[dim] = [statistics.fmean(d) for d in draws]
    return pooled


def _ablation_available() -> bool:
    run, _ = ABLATION["D3"]
    return all((RUNS / run / "rating" / f"judgments_pass_{p}.json").exists() for p in PASSES)


def _lesson_diff(treat: Cell, base: Cell, lesson: str) -> float:
    c = _contrast(treat, base, ENDPOINT)
    return float(dict(zip(c["lessons"], c["diffs"], strict=True))[lesson])


def _ablation(per_pass: dict) -> list[str]:
    """D3 against D2, read by the bands fixed before it was generated."""
    run, cond = ABLATION["D3"]
    d3 = {p: _load(run, cond, p) for p in PASSES}
    pooled = {arm: _pool([per_pass[arm][p][0] for p in PASSES]) for arm in ARMS}
    pooled["D3"] = _pool([d3[p][0] for p in PASSES])
    c = _contrast(pooled["D3"], pooled["D2"], ENDPOINT)
    if abs(c["mean"]) < ABLATION_NULL_BAND:
        reading = (
            "**within the null band** — reuse did not earn the score; the t2-w09 effect "
            "is the plan, not the copying."
        )
    elif c["mean"] <= ABLATION_EFFECT:
        reading = (
            "**at or past the effect band** — her evaluation questions contribute to "
            "judged alignment. Legitimate by the rubric guidance *and* indistinguishable "
            "here from reuse being rewarded; both readings stand, neither is chosen."
        )
    else:
        reading = "**between the bands** — reported as between, with the per-lesson diffs."
    lines = [
        "## Ablation — D3 (no assessment) against D2, pooled",
        "",
        f"Bands fixed before generation: |Δ| < {ABLATION_NULL_BAND} null; "
        f"Δ ≤ {ABLATION_EFFECT} effect.",
        "",
        "| contrast | mean Δ | +/0/− | p | per lesson |",
        "|---|---:|:-:|---:|---|",
        _fmt_contrast("**D3 − D2** (the ablation)", c),
        _fmt_contrast("D3 − D1", _contrast(pooled["D3"], pooled["D1"], ENDPOINT)),
        _fmt_contrast("D3 − D0", _contrast(pooled["D3"], pooled["D0"], ENDPOINT)),
        "",
        f"Reading: {reading}",
        "",
        "t2-w09 alone, against D0: "
        f"D2 {_lesson_diff(pooled['D2'], pooled['D0'], 't2-w09'):+.2f} → "
        f"D3 {_lesson_diff(pooled['D3'], pooled['D0'], 't2-w09'):+.2f}.",
        "",
        "### Non-inferiority — D3 − D2 on the other dimensions",
        "",
        "| dimension | mean Δ | +/0/− | p | verdict |",
        "|---|---:|:-:|---:|---|",
    ]
    for dim in DIMENSIONS[1:]:
        k = _contrast(pooled["D3"], pooled["D2"], dim)
        pos, zero, neg = k["signs"]
        pv = "—" if k["p"] is None else f"{k['p']:.3f}"
        verdict = "not inferior" if k["mean"] > -NON_INFERIORITY_MARGIN else "**inferior**"
        lines.append(f"| {dim} | {k['mean']:+.2f} | {pos}/{zero}/{neg} | {pv} | {verdict} |")
    lines += ["", "| D3 pass | overlap ρ | n |", "|---|---:|---:|"]
    for p in PASSES:
        rho, n = _overlap_rho(d3[p][1])
        lines.append(f"| {p} | {'—' if rho is None else f'{rho:+.2f}'} | {n} |")
    means = [statistics.fmean(_lesson_means(pooled["D3"], d).values()) for d in DIMENSIONS]
    lines += [
        "",
        "D3 arm means, pooled: "
        + ", ".join(f"{d} {m:.2f}" for d, m in zip(DIMENSIONS, means, strict=True)),
        "",
    ]
    return lines


def _full_available() -> bool:
    return all(
        (RUNS / run / "rating" / f"judgments_pass_{p}.json").exists()
        for run, _ in FULL_ARMS.values()
        for p in PASSES
    )


def full_contrast() -> list[str]:
    """E2 against E1 and E0, by the bands fixed before it was generated."""
    pooled = {
        arm: _pool([_load(run, cond, p)[0] for p in PASSES])
        for arm, (run, cond) in FULL_ARMS.items()
    }
    endpoint = _contrast(pooled["E2"], pooled["E1"], ENDPOINT)
    if abs(endpoint["mean"]) < FULL_NULL_BAND:
        verdict = (
            "**within the null band** — representing her plan more fully changes "
            "nothing the rubric sees."
        )
    elif endpoint["mean"] >= FULL_EFFECT:
        verdict = (
            "**at or past the effect band** — the frozen C1 was under-representing "
            "the plan, and the definition should carry these fields."
        )
    else:
        verdict = "**between the bands** — reported as between, with the per-lesson diffs."
    lines = [
        "## v7-full — every field her plan holds",
        "",
        f"Bands fixed before generation: |Δ| < {FULL_NULL_BAND} null; Δ ≥ {FULL_EFFECT} effect.",
        "E0 = C0 and E1 = C1 under the frozen definition; E2 = C1 under `v7-full`.",
        "",
        "| contrast | mean Δ | +/0/− | p | per lesson |",
        "|---|---:|:-:|---:|---|",
        _fmt_contrast("**E2 − E1** (fuller plan vs frozen)", endpoint),
        _fmt_contrast("E1 − E0 (frozen C1 vs C0)", _contrast(pooled["E1"], pooled["E0"], ENDPOINT)),
        _fmt_contrast("E2 − E0 (fuller C1 vs C0)", _contrast(pooled["E2"], pooled["E0"], ENDPOINT)),
        "",
        f"Reading: {verdict}",
        "",
        "### Non-inferiority — E2 − E1 on the other dimensions",
        "",
        "| dimension | mean Δ | +/0/− | p | verdict |",
        "|---|---:|:-:|---:|---|",
    ]
    for dim in DIMENSIONS[1:]:
        k = _contrast(pooled["E2"], pooled["E1"], dim)
        pos, zero, neg = k["signs"]
        pv = "—" if k["p"] is None else f"{k['p']:.3f}"
        ok = "not inferior" if k["mean"] > -NON_INFERIORITY_MARGIN else "**inferior**"
        lines.append(f"| {dim} | {k['mean']:+.2f} | {pos}/{zero}/{neg} | {pv} | {ok} |")
    lines += ["", "| arm | " + " | ".join(DIMENSIONS) + " |", "|---|" + "---:|" * len(DIMENSIONS)]
    for arm in FULL_ARMS:
        means = [statistics.fmean(_lesson_means(pooled[arm], d).values()) for d in DIMENSIONS]
        lines.append(f"| {arm} | " + " | ".join(f"{m:.2f}" for m in means) + " |")
    return [*lines, ""]


def report() -> str:
    per_pass = {arm: {p: _load(run, cond, p) for p in PASSES} for arm, (run, cond) in ARMS.items()}
    lines = [
        "# Diagnostic v4 — results, read as predeclared",
        "",
        "Generated by `experiments.h1_condition_eval.diagnostic_v4`; do not edit.",
        "",
        "D0 = C0 and D1 = C1 from `diag-v3` (frozen definition, new contract); D2 = C1 from",
        "`diag-v4` (`v4-activities`). Six lessons, three draws per cell, two Sonnet 4.6",
        "judge passes per candidate — repeated judgments, not replications. Each contrast",
        "is paired by lesson over the mean of draws; Wilcoxon signed-rank, two-sided; n = 6,",
        "floor p = .031.",
        "",
    ]

    for label, cells_for in (
        ("pass a", {a: per_pass[a]["a"][0] for a in ARMS}),
        ("pass b", {a: per_pass[a]["b"][0] for a in ARMS}),
        ("both passes pooled", {a: _pool([per_pass[a][p][0] for p in PASSES]) for a in ARMS}),
    ):
        lines += [
            f"## {label}",
            "",
            f"### Endpoint — {ENDPOINT}",
            "",
            "| contrast | mean Δ | +/0/− | p | per lesson |",
            "|---|---:|:-:|---:|---|",
            _fmt_contrast(
                "**D2 − D1** (the diagnostic)",
                _contrast(cells_for["D2"], cells_for["D1"], ENDPOINT),
            ),
            _fmt_contrast("D1 − D0", _contrast(cells_for["D1"], cells_for["D0"], ENDPOINT)),
            _fmt_contrast("D2 − D0", _contrast(cells_for["D2"], cells_for["D0"], ENDPOINT)),
            "",
            "### Non-inferiority — D2 − D1 on the other dimensions "
            f"(margin −{NON_INFERIORITY_MARGIN})",
            "",
            "| dimension | mean Δ | +/0/− | p | verdict |",
            "|---|---:|:-:|---:|---|",
        ]
        for dim in DIMENSIONS[1:]:
            c = _contrast(cells_for["D2"], cells_for["D1"], dim)
            pos, zero, neg = c["signs"]
            p = "—" if c["p"] is None else f"{c['p']:.3f}"
            verdict = "not inferior" if c["mean"] > -NON_INFERIORITY_MARGIN else "**inferior**"
            lines.append(f"| {dim} | {c['mean']:+.2f} | {pos}/{zero}/{neg} | {p} | {verdict} |")
        lines.append("")

    lines += [
        "## Overlap — does reusing her evaluation questions predict the alignment score?",
        "",
        f"Spearman ρ between normalised reuse and {ENDPOINT}, per arm, per pass. "
        f"Trigger: |ρ| ≥ {OVERLAP_TRIGGER}.",
        "",
        "| arm | pass | ρ | n | triggered |",
        "|---|---|---:|---:|---|",
    ]
    any_trigger = False
    for arm in ARMS:
        for p in PASSES:
            rho, n = _overlap_rho(per_pass[arm][p][1])
            hit = rho is not None and abs(rho) >= OVERLAP_TRIGGER
            any_trigger |= hit
            shown = "—" if rho is None else f"{rho:+.2f}"
            lines.append(f"| {arm} | {p} | {shown} | {n} | {'**yes**' if hit else 'no'} |")
    lines += [
        "",
        "## Arm means, pooled",
        "",
        "| arm | " + " | ".join(DIMENSIONS) + " |",
        "|---|" + "---:|" * len(DIMENSIONS),
    ]
    for arm in ARMS:
        pooled = _pool([per_pass[arm][p][0] for p in PASSES])
        means = [statistics.fmean(_lesson_means(pooled, d).values()) for d in DIMENSIONS]
        lines.append(f"| {arm} | " + " | ".join(f"{m:.2f}" for m in means) + " |")
    if _full_available():
        lines += [""] + full_contrast()
    if _ablation_available():
        lines += [""] + _ablation(per_pass)
    lines += [
        "",
        "## Predeclared triggers for the no-assessment ablation",
        "",
        f"- reuse predicts the score (|ρ| ≥ {OVERLAP_TRIGGER}) in any arm/pass: "
        + ("**fired**" if any_trigger else "not fired"),
        "- D2 omits a curriculum target C0 covers: read from the packs, reported separately",
        "- a practice set is more than half her evaluation questions: read from `_key.json`",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT.write_text(report(), encoding="utf-8")
    print(OUT.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
