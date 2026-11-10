"""The exact tests the dissertation declares, computed without approximation.

Scores are carried as fractions, so two differences that are equal in arithmetic are equal here
and share a midrank; ranking floating-point differences splits them and moves the p-value.
"""

from __future__ import annotations

import itertools
from collections.abc import Mapping, Sequence
from fractions import Fraction


def midranks(values: Sequence[Fraction]) -> list[Fraction]:
    order = sorted(range(len(values)), key=lambda index: values[index])
    ranks = [Fraction(0)] * len(values)
    start = 0
    while start < len(order):
        end = start
        while end + 1 < len(order) and values[order[end + 1]] == values[order[start]]:
            end += 1
        for position in range(start, end + 1):
            ranks[order[position]] = Fraction(start + end, 2) + 1
        start = end + 1
    return ranks


def signed_rank(differences: Sequence[Fraction]) -> tuple[float, int]:
    """One-sided exact Wilcoxon signed-rank p, zeros dropped, and the number of pairs kept."""
    kept = [difference for difference in differences if difference != 0]
    ranks = midranks([abs(difference) for difference in kept])
    observed = sum(rank for rank, difference in zip(ranks, kept, strict=True) if difference > 0)
    hits = sum(
        1
        for signs in itertools.product((0, 1), repeat=len(kept))
        if sum(rank for rank, on in zip(ranks, signs, strict=True) if on) >= observed
    )
    return hits / 2 ** len(kept), len(kept)


def signed_rank_two_sided(differences: Sequence[Fraction]) -> float:
    """Twice the smaller one-sided exact signed-rank tail, capped at 1."""
    upper, _ = signed_rank(differences)
    lower, _ = signed_rank([-difference for difference in differences])
    return min(1.0, 2 * min(upper, lower))


def sign_flip(values: Sequence[Number]) -> float:
    """One-sided exact sign-flip p on the mean of the non-zero values."""
    kept = [Fraction(value) for value in values if value != 0]
    observed = sum(kept)
    hits = sum(
        1
        for signs in itertools.product((1, -1), repeat=len(kept))
        if sum(sign * value for sign, value in zip(signs, kept, strict=True)) >= observed
    )
    return float(hits / 2 ** len(kept))


def cluster_sign_flip(by_cluster: Mapping[str, Sequence[Fraction]]) -> float:
    """One-sided p keeping the unit-average effect but flipping every unit of a cluster together."""
    totals = [sum(values, Fraction(0)) for values in by_cluster.values()]
    observed = sum(totals)
    hits = sum(
        1
        for signs in itertools.product((1, -1), repeat=len(totals))
        if sum(sign * total for sign, total in zip(signs, totals, strict=True)) >= observed
    )
    return float(hits / 2 ** len(totals))


def icc_one_way(groups: Sequence[Sequence[float]]) -> float:
    """ICC(1) from the one-way random-effects decomposition, for groups of unequal size."""
    values = [value for group in groups for value in group]
    count, total = len(groups), len(values)
    grand = sum(values) / total
    means = [sum(group) / len(group) for group in groups]
    between = sum(len(g) * (m - grand) ** 2 for g, m in zip(groups, means, strict=True)) / (
        count - 1
    )
    within = sum((v - m) ** 2 for g, m in zip(groups, means, strict=True) for v in g) / (
        total - count
    )
    k0 = (total - sum(len(group) ** 2 for group in groups) / total) / (count - 1)
    return (between - within) / (between + (k0 - 1) * within)


Number = int | float | Fraction
