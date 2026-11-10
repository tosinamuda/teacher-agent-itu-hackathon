"""The crossed mixed model behind the condition contrasts the dissertation reports.

The declared test reduces every score to six paired lesson differences. That estimator
cannot see the rater term it averages over. This fits all observations at once, crossed by
rater, lesson, objective and pack with a further rater-by-condition term, so the rater
variance is estimated and a condition effect arrives with an interval.

Two traps live in this fit, and each has produced numbers that looked publishable and
were not.

The first is the pack key. ``internal_packet_id`` carries a ``-c1``/``-c2`` copy suffix
that distinguishes the two raters' copies of one pack. Grouping on it splits every pack in
two, collapses the pack term to near zero and pushes that variance into the rater and
objective terms. The pack random effect must group both ratings of a pack together.

The second is convergence. The design is near-singular -- several variance terms sit close
to zero -- so the likelihood surface is flat enough for an optimiser to stop on a ledge and
report from there. On the lesson-context endpoint two optimisers reach -443.22 while two
stop short, one of them 11.6 units away with an interval a fifth wider and a variance
decomposition that inverts the ordering of the terms. Every fit here is therefore attempted
under several optimisers and the converged one with the highest log-likelihood wins; if
none converges it raises rather than returning a number that reads as fine.

Every specification Appendix D reports is named in ``SPECIFICATIONS``: the two reported fits,
the primary endpoint adjusted for pack length, and the three refits of the secondary measure
without its boundary components. The results register fits them from the study workbook and
writes them into it; this module's own report prints them from a ratings export::

    uv run python -m experiments.human_rating.mixed_model ratings.xlsx
"""

from __future__ import annotations

import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: Tried in order; the converged fit with the highest log-likelihood is the one reported.
OPTIMISERS: tuple[str, ...] = ("powell", "cg", "lbfgs", "bfgs")

#: Crossed variance components. ``packet`` keys on the pack, not on a rater's copy of it.
VARIANCE_COMPONENTS: dict[str, str] = {
    "rater": "0 + C(rater)",
    "lesson": "0 + C(lesson)",
    "objective": "0 + C(objective)",
    "packet": "0 + C(packet)",
    "rater_by_condition": "0 + C(rater_condition)",
}

#: The criterion column is an index into the printed order of the Part 1 instrument.
LESSON_CONTEXT_CRITERION = 2

#: Pack length enters the model in thousands of characters, the unit Appendix D prints.
LENGTH_TERM = "length_k"

_Z_TWO_SIDED = 1.9600
_Z_ONE_SIDED = 1.6449
_Z_POWER = {0.80: 0.8416, 0.90: 1.2816}


class ConvergenceError(RuntimeError):
    """No optimiser reached a converged solution, so no interval is reportable."""


@dataclass(frozen=True)
class Specification:
    """One model Appendix D reports: its data, fixed effects and variance components."""

    name: str
    label: str
    formula: str
    primary_endpoint: bool
    components: tuple[str, ...] = tuple(VARIANCE_COMPONENTS)


SECONDARY = Specification(
    "secondary", "secondary pooled measure", "score ~ C(condition) + C(criterion)", False
)
PRIMARY = Specification("primary", "primary endpoint", "score ~ C(condition)", True)
PRIMARY_LENGTH = Specification(
    "primary-length",
    "primary endpoint, adjusted for pack length",
    f"score ~ C(condition) + {LENGTH_TERM}",
    True,
)
SECONDARY_REFITS = (
    Specification(
        "secondary-without-objective",
        "secondary pooled measure, without the objective component",
        SECONDARY.formula,
        False,
        ("rater", "lesson", "packet", "rater_by_condition"),
    ),
    Specification(
        "secondary-without-rater-by-condition",
        "secondary pooled measure, without the rater-by-condition component",
        SECONDARY.formula,
        False,
        ("rater", "lesson", "objective", "packet"),
    ),
    Specification(
        "secondary-rater-lesson-pack",
        "secondary pooled measure, with rater, lesson and pack alone",
        SECONDARY.formula,
        False,
        ("rater", "lesson", "packet"),
    ),
)
SPECIFICATIONS = (SECONDARY, PRIMARY, PRIMARY_LENGTH, *SECONDARY_REFITS)


@dataclass(frozen=True)
class Term:
    """One fixed effect: a condition against the C0 baseline, or a covariate."""

    name: str
    estimate: float
    low: float
    high: float
    p_value: float
    standard_error: float


@dataclass(frozen=True)
class Fit:
    """A converged fit, with everything the dissertation quotes from it."""

    label: str
    observations: int
    optimiser: str
    converged: tuple[str, ...]
    log_likelihood: float
    shares: dict[str, float]
    contrasts: list[Term]
    covariates: list[Term]
    #: What statsmodels warned while reaching this fit, such as a component on its boundary.
    warnings: tuple[str, ...] = ()

    def contrast(self, condition: str) -> Term:
        for item in self.contrasts:
            if item.name == condition:
                return item
        raise KeyError(f"no contrast for {condition}")


def scores(path: Path) -> Any:
    """The H1 scores of a ratings export, with the keys the model groups on."""
    import openpyxl
    import pandas as pd

    page = openpyxl.load_workbook(path, read_only=True, data_only=True)["H1 scores"]
    rows = list(page.iter_rows(values_only=True))
    return _keyed(pd.DataFrame(rows[1:], columns=[str(head) for head in rows[0]]))


#: The study workbook's raw Part 1 columns under the names a ratings export gives them.
WORKBOOK_COLUMNS = {
    "rater_id": "rater",
    "lesson_id": "lesson",
    "objective_id": "lesson_objective_id",
    "criterion_index": "criterion",
}


def workbook_scores(ratings: list[dict[str, Any]], generation: list[dict[str, Any]]) -> Any:
    """The study workbook's answered Part 1 ratings, keyed, with each pack's length joined."""
    import pandas as pd

    answered = [r for r in ratings if r["response_status"] == "answered"]
    frame = _keyed(pd.DataFrame(answered).rename(columns=WORKBOOK_COLUMNS))
    characters = {(g["lesson"], g["condition"], g["repeat"]): g["chars"] for g in generation}
    keys = zip(frame["lesson"], frame["condition"], frame["draw"], strict=True)
    frame[LENGTH_TERM] = [characters[key] / 1000 for key in keys]
    return frame


def _keyed(frame: Any) -> Any:
    frame = frame[frame["score"].notna()].copy()
    frame["score"] = frame["score"].astype(float)
    frame["objective"] = frame["lesson"] + "/" + frame["lesson_objective_id"].astype(str)
    frame["rater_condition"] = frame["rater"] + ":" + frame["condition"]
    frame["packet"] = frame["internal_packet_id"].str.replace(r"-c\d+$", "", regex=True)
    frame["one"] = 1
    return frame


def fit(specification: Specification, data: Any) -> Fit:
    """One named specification, on the primary endpoint's rows where it asks for them."""
    if specification.primary_endpoint:
        data = data[data["criterion"] == LESSON_CONTEXT_CRITERION]
    components = {name: VARIANCE_COMPONENTS[name] for name in specification.components}
    return fit_crossed(data, specification.formula, specification.label, components)


def fit_crossed(
    data: Any, formula: str, label: str, components: dict[str, str] = VARIANCE_COMPONENTS
) -> Fit:
    """Fit under every optimiser and keep the converged solution that fits best."""
    import numpy as np
    import statsmodels.formula.api as smf

    reached = []
    for optimiser in OPTIMISERS:
        model = smf.mixedlm(
            formula, data, groups=data["one"], re_formula="0", vc_formula=components
        )
        try:
            with warnings.catch_warnings(record=True) as raised:
                warnings.simplefilter("always")
                result = model.fit(reml=True, method=optimiser)
        except np.linalg.LinAlgError:
            # A flat surface can send one optimiser into a singular Hessian while the
            # others land cleanly. One failure is not the fit failing.
            continue
        if result.converged:
            said = tuple(dict.fromkeys(str(w.message) for w in raised))
            reached.append((result.llf, optimiser, model, result, said))

    if not reached:
        raise ConvergenceError(
            f"{label}: none of {', '.join(OPTIMISERS)} converged on {len(data)} observations"
        )

    log_likelihood, optimiser, model, result, said = max(reached, key=lambda found: found[0])
    return Fit(
        label=label,
        observations=len(data),
        optimiser=optimiser,
        converged=tuple(found[1] for found in reached),
        log_likelihood=float(log_likelihood),
        shares=_shares(model, result),
        contrasts=[t for t in _terms(result) if t.name.startswith("C")],
        covariates=[t for t in _terms(result) if not t.name.startswith("C")],
        warnings=said,
    )


def _shares(model: Any, result: Any) -> dict[str, float]:
    """Each variance component as a share of the total, residual included."""
    parts = dict(zip(model.exog_vc.names, (float(v) for v in result.vcomp), strict=True))
    parts["residual"] = float(result.scale)
    total = sum(parts.values())
    return {name: value / total for name, value in parts.items()}


def _terms(result: Any) -> list[Term]:
    """Every fixed effect but the intercept and the criterion levels, which no one reports."""
    interval = result.conf_int()
    return [
        Term(
            name=name.split("T.")[-1].rstrip("]"),
            estimate=float(result.params[name]),
            low=float(interval.loc[name][0]),
            high=float(interval.loc[name][1]),
            p_value=float(result.pvalues[name]),
            standard_error=float(result.bse[name]),
        )
        for name in result.params.index
        if (name.startswith("C(condition)") and ":" not in name) or name == LENGTH_TERM
    ]


def minimum_detectable_effect(
    standard_error: float, *, power: float = 0.80, one_sided: bool = False
) -> float:
    """The smallest effect this design could separate from zero, in scale points."""
    alpha = _Z_ONE_SIDED if one_sided else _Z_TWO_SIDED
    return (alpha + _Z_POWER[power]) * standard_error


def report(path: Path) -> None:
    data = scores(path)
    print(f"═══ {len(data)} human scores from {path.name}, {data['packet'].nunique()} packs ═══")

    for found in (fit(SECONDARY, data), fit(PRIMARY, data)):
        print(f"\n── {found.label}: {found.observations} observations ──")
        print(f"   {found.optimiser}, log-likelihood {found.log_likelihood:.2f}")
        for name, share in sorted(found.shares.items(), key=lambda part: -part[1]):
            print(f"   {name:22s} {share:6.1%}")
        for item in found.contrasts:
            print(
                f"   {item.name} − C0 = {item.estimate:+.3f}"
                f"   95% CI [{item.low:+.3f}, {item.high:+.3f}]   p = {item.p_value:.3f}"
            )
        error = found.contrast("C3").standard_error
        print(f"   SE of C3 − C0 {error:.4f}")
        print(f"   minimum detectable effect {minimum_detectable_effect(error):.2f} scale points")
        print(f"   one-sided {minimum_detectable_effect(error, one_sided=True):.2f}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    report(Path(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
