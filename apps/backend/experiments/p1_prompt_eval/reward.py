"""The reward function for manually judging personalised sections.

The judge READS each output (human or human-proxy — never the generating
model) and scores every criterion on its anchored scale; this module owns the
weights and the arithmetic so judgements are comparable across cases, runs and
judges. Max score 12.

Criteria (anchors):

- objective_preservation (0-2): 2 = same objective, scope unchanged;
  1 = drift (adds/loses scope); 0 = teaches something else.
- misconception_targeting (0-3): 3 = names and defuses the learner's ACTUAL
  chosen distractor(s) and teaches a transferable check; 2 = addresses the
  slip-category but not the actual distractor; 1 = generic re-teaching with a
  nod to the misconception; 0 = ignores it. For objectives with NO
  misconception (extend/mastered): 3 = correctly adds challenge instead of
  fake remediation; 0 = invents remediation.
- support_calibration (0-2): 2 = depth/hints/practice match the band and the
  learner's own survey answers (remediate -> step-by-step + easier on-ramp;
  extend -> stretch, less redundancy); 1 = partially; 0 = mismatched.
- tone_audience (0-1): 1 = gentle and impersonal ("a common slip…"), never
  echoes the learner's own answers; 0 = any violation.
- grounding_fidelity (0-3): 3 = claims consistent with the provided evidence,
  refs only where content is drawn from it, no invented source claims;
  2 = decorative/over-broad refs but no false claims; 1 = an invented source
  claim or a misattribution; 0 = fabricated content (including wrong maths).
- actionable_practice (0-1): 1 = leaves genuinely unsolved practice for the
  learner; 0 = prints the solutions inline / no practice at all.

Usage: fill ``judgements/<compare-dir>.json`` as
{"case_id": {"objective_id": {"A": {criterion: score}, "B": {...},
"notes": "..."}}} then run this module to aggregate:

    uv run python -m experiments.p1_prompt_eval.reward <judgements.json> <key.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean

CRITERIA: dict[str, int] = {
    "objective_preservation": 2,
    "misconception_targeting": 3,
    "support_calibration": 2,
    "tone_audience": 1,
    "grounding_fidelity": 3,
    "actionable_practice": 1,
}
MAX_SCORE = sum(CRITERIA.values())


def reward(scores: dict[str, int]) -> float:
    """Sum the criterion scores after validating each against its scale."""
    total = 0
    for criterion, ceiling in CRITERIA.items():
        value = scores[criterion]
        if not 0 <= value <= ceiling:
            raise ValueError(f"{criterion}={value} outside 0..{ceiling}")
        total += value
    return float(total)


def aggregate(judgements: dict, key: dict) -> dict:
    """Per-run mean reward + per-criterion means, decoded via the blinding key."""
    per_run: dict[str, list[float]] = {}
    per_criterion: dict[str, dict[str, list[int]]] = {}
    for case_id, objectives in judgements.items():
        labels = key[case_id]
        for scores_by_candidate in objectives.values():
            for candidate in ("A", "B"):
                if candidate not in scores_by_candidate:
                    continue
                run = labels[f"Candidate {candidate}"]
                scores = scores_by_candidate[candidate]
                per_run.setdefault(run, []).append(reward(scores))
                for criterion in CRITERIA:
                    per_criterion.setdefault(run, {}).setdefault(criterion, []).append(
                        scores[criterion]
                    )
    return {
        "max_score": MAX_SCORE,
        "n_judged": {run: len(values) for run, values in per_run.items()},
        "mean_reward": {run: round(mean(values), 2) for run, values in per_run.items()},
        "per_criterion_mean": {
            run: {c: round(mean(v), 2) for c, v in criteria.items()}
            for run, criteria in per_criterion.items()
        },
    }


def main() -> None:
    judgements = json.loads(Path(sys.argv[1]).read_text())
    key = json.loads(Path(sys.argv[2]).read_text())
    # Notes ride alongside scores; strip them before aggregating.
    cleaned = {
        case_id: {
            objective: {k: v for k, v in scores.items() if k in ("A", "B")}
            for objective, scores in objectives.items()
        }
        for case_id, objectives in judgements.items()
    }
    print(json.dumps(aggregate(cleaned, key), indent=2))


if __name__ == "__main__":
    main()
