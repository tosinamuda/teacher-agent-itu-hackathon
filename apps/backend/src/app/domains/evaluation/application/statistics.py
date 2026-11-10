"""Statistical helpers for the H1/H2 results analysis (pure functions, no DB)."""

from __future__ import annotations

import numpy as np


def summarize(scores: list[float]) -> dict:
    """N / mean / std for a group of scores (std is the sample SD; None when n<2)."""
    if not scores:
        return {"n": 0, "mean": None, "std": None}
    arr = np.asarray(scores, dtype=float)
    return {
        "n": int(arr.size),
        "mean": round(float(arr.mean()), 4),
        "std": round(float(arr.std(ddof=1)), 4) if arr.size > 1 else None,
    }


def cliffs_delta(a: list[float], b: list[float]) -> float | None:
    """Cliff's delta effect size for a vs b in [-1, 1] (non-parametric, ordinal-safe)."""
    if not a or not b:
        return None
    greater = sum(1 for x in a for y in b if x > y)
    less = sum(1 for x in a for y in b if x < y)
    return round((greater - less) / (len(a) * len(b)), 4)


def cohens_d(a: list[float], b: list[float]) -> float | None:
    """Cohen's d (pooled SD) for a vs b; None when insufficient/zero-variance data."""
    if len(a) < 2 or len(b) < 2:
        return None
    arr_a, arr_b = np.asarray(a, float), np.asarray(b, float)
    pooled_var = ((arr_a.size - 1) * arr_a.var(ddof=1) + (arr_b.size - 1) * arr_b.var(ddof=1)) / (
        arr_a.size + arr_b.size - 2
    )
    if pooled_var <= 0:
        return None
    return round(float((arr_a.mean() - arr_b.mean()) / np.sqrt(pooled_var)), 4)


def mann_whitney_p(a: list[float], b: list[float]) -> float | None:
    """Two-sided Mann-Whitney U p-value for a vs b; None when a test isn't computable."""
    if len(a) < 2 or len(b) < 2:
        return None
    try:
        from scipy.stats import mannwhitneyu

        return round(float(mannwhitneyu(a, b, alternative="two-sided").pvalue), 4)
    except Exception:  # noqa: BLE001
        return None


def wilcoxon_p(treatment: list[float], baseline: list[float]) -> float | None:
    """Two-sided Wilcoxon signed-rank p-value for PAIRED treatment vs baseline.

    The paired counterpart to :func:`mann_whitney_p`: ``treatment[i]`` and
    ``baseline[i]`` are the same rater's P1 (candidate) and P0 (base) scores for one
    H2 rating. Returns None when not computable (mismatched/short input, or every
    pair is tied so the signed-rank statistic is undefined).
    """
    if len(treatment) != len(baseline) or len(treatment) < 2:
        return None
    if all(t == b for t, b in zip(treatment, baseline, strict=True)):
        return None
    try:
        from scipy.stats import wilcoxon

        return round(float(wilcoxon(treatment, baseline, alternative="two-sided").pvalue), 4)
    except Exception:  # noqa: BLE001
        return None


def kruskal_p(groups: list[list[float]]) -> float | None:
    """Kruskal-Wallis p across >=2 non-empty groups (the C0-C3 omnibus test)."""
    usable = [g for g in groups if len(g) >= 1]
    if len(usable) < 2 or sum(len(g) for g in usable) < 4:
        return None
    try:
        from scipy.stats import kruskal

        return round(float(kruskal(*usable).pvalue), 4)
    except Exception:  # noqa: BLE001
        return None


def krippendorff_alpha(rater_by_item: list[list[float | None]]) -> float | None:
    """Krippendorff's alpha (ordinal) over a raters x items matrix; None if not computable."""
    if len(rater_by_item) < 2:
        return None
    try:
        import krippendorff

        data = [[np.nan if v is None else v for v in row] for row in rater_by_item]
        # Need at least some item rated by >=2 raters for alpha to be defined.
        alpha = krippendorff.alpha(reliability_data=data, level_of_measurement="ordinal")
        return None if alpha is None or np.isnan(alpha) else round(float(alpha), 4)
    except Exception:  # noqa: BLE001
        return None
