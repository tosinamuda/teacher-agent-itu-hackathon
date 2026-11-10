"""Study results described, for one lesson or across a study's lessons.

Part 1 is means, score spreads and favourable shares by condition, Part 2 choices counted,
and across lessons each objective is also a data point.

Descriptive only: every rater and draw pooled. The study's tests are the thesis's business,
not this view's.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from typing import NamedTuple

#: The lowest score the study counts as favourable, as the thesis reports its shares.
FAVOURABLE = 4


class RatedScore(NamedTuple):
    """One Part 1 score: the note's condition, the criterion, and who scored which cell."""

    condition: str
    criterion_id: str
    score: int
    #: What was scored: one note's objective.
    cell: tuple[str, str]
    rater: str


@dataclass(frozen=True)
class ConditionMean:
    """Part 1: one criterion's scores for one condition's notes, described."""

    condition: str
    criterion_id: str
    mean: float
    n: int
    #: How many scores were 1, 2, 3, 4 and 5.
    score_counts: list[int]
    #: Cells two raters scored, and those both scored favourably.
    double_rated: int
    both_favourable: int


@dataclass(frozen=True)
class ChoiceCount:
    """Part 2: how often one criterion's comparison came out one way."""

    criterion_id: str
    #: P1, P0, or ``neither``.
    favoured: str
    #: ``clearly`` or ``slightly``; none when neither note was favoured.
    strength: str | None
    count: int


@dataclass(frozen=True)
class LessonResults:
    part_1: list[ConditionMean]
    part_2: list[ChoiceCount]


@dataclass(frozen=True)
class ObjectiveMean:
    """One lesson objective's mean score for one condition, over every rater, draw and criterion."""

    lesson: str
    objective_id: str
    objective_text: str | None
    condition: str
    mean: float
    n: int


@dataclass(frozen=True)
class StudyResults:
    """A study's ratings described across its lessons, and each objective as a data point."""

    part_1: list[ConditionMean]
    objectives: list[ObjectiveMean]
    part_2: list[ChoiceCount]


def objective_means(
    scores: Iterable[tuple[str, str, str, int]], texts: dict[str, str]
) -> list[ObjectiveMean]:
    """Each (lesson, objective, condition)'s mean over its rows of those three and a score."""
    totals: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for lesson, objective_id, condition, score in scores:
        totals[(lesson, objective_id, condition)].append(score)
    return [
        ObjectiveMean(
            lesson,
            objective_id,
            texts.get(objective_id),
            condition,
            sum(values) / len(values),
            len(values),
        )
        for (lesson, objective_id, condition), values in sorted(totals.items())
    ]


def _described(condition: str, criterion_id: str, scores: list[RatedScore]) -> ConditionMean:
    values = [score.score for score in scores]
    raters_of: dict[tuple[str, str], dict[str, int]] = defaultdict(dict)
    for score in scores:
        raters_of[score.cell][score.rater] = score.score
    pairs = [by_rater.values() for by_rater in raters_of.values() if len(by_rater) == 2]
    return ConditionMean(
        condition,
        criterion_id,
        sum(values) / len(values),
        len(values),
        score_counts=[values.count(point) for point in range(1, 6)],
        double_rated=len(pairs),
        both_favourable=sum(all(value >= FAVOURABLE for value in pair) for pair in pairs),
    )


def part_1_means(scores: Iterable[RatedScore]) -> list[ConditionMean]:
    """Each (condition, criterion)'s scores described: mean, spread and paired favourable."""
    grouped: dict[tuple[str, str], list[RatedScore]] = defaultdict(list)
    for score in scores:
        grouped[(score.condition, score.criterion_id)].append(score)
    return [
        _described(condition, criterion_id, group)
        for (condition, criterion_id), group in sorted(grouped.items())
    ]


def _strength(choice: str) -> str | None:
    for strength in ("clearly", "slightly"):
        if strength in choice.lower():
            return strength
    return None


def part_2_counts(judgements: Iterable[tuple[str, str, str]]) -> list[ChoiceCount]:
    """Each criterion's ``(criterion, choice, favoured)`` judgements, counted by outcome."""
    counts = Counter(
        (criterion_id, favoured, _strength(choice) if favoured != "neither" else None)
        for criterion_id, choice, favoured in judgements
    )
    return [
        ChoiceCount(criterion_id, favoured, strength, count)
        for (criterion_id, favoured, strength), count in sorted(
            counts.items(), key=lambda item: (item[0][0], item[0][1], item[0][2] or "")
        )
    ]
