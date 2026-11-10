"""The judged scores for a run, keyed the way the trace is: lesson, condition, draw.

A run's rating directory holds one or more archived judge passes and a blinding
key. This joins them so a document that shows a pack can put that pack's own
scores beside it, and the cell's mean over draws beside those — the two numbers
a reader needs to connect what they just read to what the study counted.
"""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from pathlib import Path

from app.domains.evaluation.application.constants import H1_RUBRIC

DIMENSIONS: tuple[str, ...] = tuple(str(c["criterion_id"]) for c in H1_RUBRIC)
LABELS: dict[str, str] = {str(c["criterion_id"]): str(c["label"]) for c in H1_RUBRIC}

Key = tuple[str, str, int]  # lesson, condition, repeat


@dataclass(frozen=True)
class RunScores:
    run: str
    passes: tuple[str, ...]
    by_draw: dict[Key, dict[str, float]]  # mean over passes
    #: Every rationale the judge wrote, by lesson/condition/dimension. A score with no
    #: reason beside it cannot be argued with, and the reason is the part a supervisor
    #: reads: the number says what happened, the sentence says why.
    reasons: dict[tuple[str, str, str], list[str]]

    def draw(self, lesson: str, condition: str, repeat: int) -> dict[str, float] | None:
        return self.by_draw.get((lesson, condition, repeat))

    def cell_mean(self, lesson: str, condition: str) -> dict[str, float] | None:
        draws = [
            v for (les, cond, _), v in self.by_draw.items() if les == lesson and cond == condition
        ]
        if not draws:
            return None
        return {d: statistics.fmean(x[d] for x in draws) for d in DIMENSIONS}

    def why(self, lesson: str, condition: str, dimension: str) -> list[str]:
        return self.reasons.get((lesson, condition, dimension), [])

    def draws_in(self, lesson: str, condition: str) -> int:
        return sum(1 for (les, cond, _) in self.by_draw if les == lesson and cond == condition)


def load_scores(run_dir: Path) -> RunScores | None:
    rating = run_dir / "rating"
    key_path = rating / "_key.json"
    passes = sorted(rating.glob("judgments_pass_*.json"))
    if not key_path.exists() or not passes:
        return None
    key = {r["candidate_id"]: r for r in json.loads(key_path.read_text())}
    per_pass: dict[Key, list[dict[str, float]]] = {}
    reasons: dict[tuple[str, str, str], list[str]] = {}
    for path in passes:
        for j in json.loads(path.read_text())["judgments"]:
            row = key[j["candidate_id"]]
            scores = {d: float(j[d]["score"]) for d in DIMENSIONS}
            per_pass.setdefault((row["lesson"], row["condition"], int(row["repeat"])), []).append(
                scores
            )
            for d in DIMENSIONS:
                if text := str(j[d].get("rationale") or "").strip():
                    seen = reasons.setdefault((row["lesson"], row["condition"], d), [])
                    if text not in seen:
                        seen.append(text)
    by_draw = {
        k: {d: statistics.fmean(s[d] for s in judged) for d in DIMENSIONS}
        for k, judged in per_pass.items()
    }
    return RunScores(
        run=run_dir.name,
        passes=tuple(p.stem.removeprefix("judgments_pass_") for p in passes),
        by_draw=by_draw,
        reasons=reasons,
    )
