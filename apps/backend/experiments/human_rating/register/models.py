"""Appendix D's crossed mixed models, fitted from the workbook and written as ``61_Mixed_Models``.

Every specification in ``mixed_model.SPECIFICATIONS`` is fitted from the answered ratings in
``10_P1_Raw``, with pack length joined from ``18_Generation_Raw``. The sheet carries each fit's
fixed effects, variance shares, optimisers and warnings; the register checks the figures
Appendix D prints against the same fits.
"""

from __future__ import annotations

from functools import cache
from typing import Any

from .. import mixed_model
from ..mixed_model import OPTIMISERS, Fit, Specification, Term
from .record import Printed, Result, agrees
from .sources import Sources
from .xlsx import Sheet

SHEET = "61_Mixed_Models"
RAW = "10_P1_Raw"
GENERATION = "18_Generation_Raw"
COMPUTED_FROM = f"{RAW}; {GENERATION} (pack length); fits in {SHEET}"

TITLE = "MIXED MODELS | APPENDIX D'S CROSSED RANDOM-EFFECTS FITS"
NOTE = (
    "Every crossed mixed model Appendix D reports, fitted by REML from the answered ratings in "
    f"{RAW}: the secondary pooled measure, the primary lesson-context endpoint, the primary "
    "endpoint with pack length (thousands of characters, from "
    f"{GENERATION}), and three refits of the secondary measure without its boundary components. "
    "Each fit is tried under four optimisers and the converged fit with the highest "
    "log-likelihood is kept; 'Converged optimisers' lists every one that converged. The pack "
    "component groups both raters' copies of a pack. Written by "
    "experiments.human_rating.register in the code repository."
)
HEADER = (
    "Fit",
    "Measure",
    "Fixed effects",
    "Variance components",
    "Observations",
    "Optimiser",
    "Converged optimisers",
    "Log-likelihood",
    "Quantity",
    "Term",
    "Estimate",
    "95% CI low",
    "95% CI high",
    "p",
    "Standard error",
    "Warnings",
)
WIDTHS = (30, 44, 30, 40, 12, 12, 26, 14, 26, 20, 12, 12, 12, 10, 12, 40)


@cache
def fits(sources: Sources) -> dict[str, Fit]:
    data = mixed_model.workbook_scores(sources.sheet(RAW), sources.sheet(GENERATION))
    return {spec.name: mixed_model.fit(spec, data) for spec in mixed_model.SPECIFICATIONS}


def sheet(sources: Sources) -> Sheet:
    found = fits(sources)
    rows = [row for spec in mixed_model.SPECIFICATIONS for row in _rows(spec, found[spec.name])]
    return Sheet(SHEET, TITLE, NOTE, HEADER, rows, WIDTHS)


def _rows(spec: Specification, fit: Fit) -> list[tuple[object, ...]]:
    described = (
        spec.name,
        fit.label,
        spec.formula.split("~ ", 1)[1],
        ", ".join(spec.components),
        fit.observations,
        fit.optimiser,
        ", ".join(fit.converged),
        fit.log_likelihood,
    )
    warned = "; ".join(fit.warnings)
    terms = [
        (*described, "fixed effect", _term_name(t), t.estimate, t.low, t.high, t.p_value)
        + (t.standard_error, warned)
        for t in [*fit.contrasts, *fit.covariates]
    ]
    shares = [
        (*described, "share of variance", name, share, None, None, None, None, warned)
        for name, share in sorted(fit.shares.items(), key=lambda part: -part[1])
    ]
    detectable = mixed_model.minimum_detectable_effect(fit.contrast("C3").standard_error)
    effect = (*described, "minimum detectable effect, 80% power, two-sided", "C3 − C0")
    return [*terms, *shares, (*effect, detectable, None, None, None, None, warned)]


def _term_name(term: Term) -> str:
    return f"{term.name} − C0" if term.name.startswith("C") else term.name


# What Appendix D prints for each condition: estimate, interval, p.
PRINTED = {
    "secondary": {
        "C1": ("+0.058", "-0.182", "+0.299", "0.634"),
        "C2": ("+0.104", "-0.137", "+0.345", "0.398"),
        "C3": ("+0.153", "-0.088", "+0.394", "0.213"),
    },
    "primary": {
        "C1": ("+0.072", "-0.257", "+0.401", ".669"),
        "C2": ("+0.250", "-0.080", "+0.580", ".138"),
        "C3": ("+0.308", "-0.021", "+0.637", ".067"),
    },
}
SHARES_PRINTED = {
    "secondary": (
        ("residual", "70.9%"),
        ("rater", "12.4%"),
        ("packet", "8.8%"),
        ("lesson", "4.4%"),
        ("rater_by_condition", "2.8%"),
        ("objective", "0.8%"),
    ),
    "primary": (
        ("residual", "76.8%"),
        ("rater", "7.5%"),
        ("rater_by_condition", "5.7%"),
        ("lesson", "4.4%"),
        ("packet", "3.1%"),
        ("objective", "2.5%"),
    ),
}
#: Appendix D gives each estimate's range across the refits: C1, C2 and C3 against C0.
REFIT_RANGES = (("+0.058", "+0.059"), ("+0.104", "+0.105"), ("+0.153", "+0.154"))
#: Appendix D's C3 against C0 interval for the two refits that drop rater-by-condition.
REFIT_INTERVALS = {
    "secondary-without-rater-by-condition": ("-0.018", "+0.325"),
    "secondary-rater-lesson-pack": ("-0.017", "+0.325"),
}


def _row(**fields: Any) -> Result:
    return Result(part="Appendix D", computed_from=COMPUTED_FROM, **fields)


def results(sources: Sources) -> list[Result]:
    found = fits(sources)
    return [
        *_reported(sources, found, "secondary"),
        *_reported(sources, found, "primary"),
        _detectable(sources, found["primary"]),
        *_refits(sources, found),
    ]


def _reported(sources: Sources, found: dict[str, Fit], name: str) -> list[Result]:
    fit = found[name]
    table = "tab:mixed-model" if name == "secondary" else "tab:mixed-model-primary"
    common = {
        "question": f"Crossed mixed model, {name} measure",
        "location": sources.where("app:mixed-model", table),
        "test": "crossed random effects, REML",
    }
    rows = [
        _row(
            id=f"D-M-{name}-{condition}",
            quantity=f"{condition} − C0",
            estimate=Printed(effect, fit.contrast(condition).estimate),
            interval=(
                Printed(low, fit.contrast(condition).low),
                Printed(high, fit.contrast(condition).high),
            ),
            p=Printed(p, fit.contrast(condition).p_value),
            sidedness="two-sided",
            unit=f"rating ({fit.observations:,})",
            **common,
        )
        for condition, (effect, low, high, p) in PRINTED[name].items()
    ]
    shares = tuple((part, Printed(text, fit.shares[part])) for part, text in SHARES_PRINTED[name])
    rows.append(
        _row(
            id=f"D-M-{name}-variance",
            quantity="Share of variance by component",
            estimate=shares[0][1],
            also=shares[1:],
            unit="variance component",
            note="; ".join(fit.warnings),
            **common,
        )
    )
    return rows


def _detectable(sources: Sources, primary: Fit) -> Result:
    error = primary.contrast("C3").standard_error
    return _row(
        id="D-M-mde",
        question="Crossed mixed model, primary endpoint",
        location=sources.where("app:mixed-model"),
        quantity="Minimum detectable effect, 80% power, two-sided",
        estimate=Printed("0.47", mixed_model.minimum_detectable_effect(error)),
        also=(
            ("standard error of C3 − C0", Printed("0.168", error)),
            ("converged log-likelihood", Printed("-443.22", primary.log_likelihood)),
            ("optimisers reaching it", Printed("2 of 4", _converged(primary))),
        ),
        unit="scale point",
    )


def _converged(fit: Fit) -> str:
    return f"{len(fit.converged)} of {len(OPTIMISERS)}"


def _refits(sources: Sources, found: dict[str, Fit]) -> list[Result]:
    rows = []
    for spec in mixed_model.SECONDARY_REFITS:
        fit = found[spec.name]
        c1, c2, c3 = (fit.contrast(c) for c in ("C1", "C2", "C3"))
        printed = REFIT_INTERVALS.get(spec.name)
        rows.append(
            _row(
                id=f"D-M-refit-{spec.name.removeprefix('secondary-')}",
                question="Crossed mixed model, secondary measure",
                location=sources.where("app:mixed-model"),
                quantity=f"C3 − C0, {fit.label.split(', ', 1)[1]}",
                estimate=_in_range(REFIT_RANGES[2], c3.estimate),
                interval=(Printed(printed[0], c3.low), Printed(printed[1], c3.high))
                if printed
                else None,
                also=(
                    ("C1 − C0", _in_range(REFIT_RANGES[0], c1.estimate)),
                    ("C2 − C0", _in_range(REFIT_RANGES[1], c2.estimate)),
                ),
                test="crossed random effects, REML",
                unit=f"rating ({fit.observations:,})",
                note="Appendix D gives each estimate's range across the three refits; the "
                "figure shown is the end of that range this refit reaches"
                + (f"; statsmodels warned: {'; '.join(fit.warnings)}" if fit.warnings else ""),
            )
        )
    return rows


def _in_range(ends: tuple[str, str], value: float) -> Printed:
    """The end of a printed range the value rounds to, or the range if it rounds to neither."""
    return Printed(next((end for end in ends if agrees(value, end)), " to ".join(ends)), value)


def length(sources: Sources) -> Result:
    """C3 against C0 on the primary endpoint with pack length held in the model."""
    fit = fits(sources)["primary-length"]
    c3, length = fit.contrast("C3"), fit.covariates[0]
    return _row(
        id="D-L3",
        question="Pack length",
        location=sources.where("app:pack-length"),
        quantity="C3 − C0 with pack length in the crossed model, primary endpoint",
        estimate=Printed("+0.290", c3.estimate),
        interval=(Printed("-0.067", c3.low), Printed("+0.647", c3.high)),
        p=Printed(".112", c3.p_value),
        sidedness="two-sided",
        test="crossed random effects, REML; sensitivity analysis",
        also=(
            ("length coefficient per thousand characters", Printed("-0.007", length.estimate)),
            ("its interval, low", Printed("-0.065", length.low)),
            ("high", Printed("+0.050", length.high)),
            ("optimisers converged", Printed("2 of 4", _converged(fit))),
        ),
        unit=f"rating ({fit.observations:,})",
    )
