"""Blinded side-by-side comparison of two prompt-version runs, for manual review.

For every case both runs cover, writes ``compare/<runA>__vs__<runB>/<case>.md``
showing Candidate A and Candidate B per objective — which run is which is
decided per case by a hash, and recorded ONLY in ``key.json``. Read the
markdown, judge each case, then open the key.

Usage:
    cd apps/backend
    uv run python -m experiments.p1_prompt_eval.compare <run-label-A> <run-label-B>
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from experiments.p1_prompt_eval.runner import RUNS_DIR, _section_markdown

COMPARE_DIR = Path(__file__).parent / "compare"


def _load_run(label: str) -> dict:
    data = json.loads((RUNS_DIR / label / "run.json").read_text())
    return {case["case_id"]: case for case in data["cases"]}


def compare(label_a: str, label_b: str) -> Path:
    runs = {label_a: _load_run(label_a), label_b: _load_run(label_b)}
    out_dir = COMPARE_DIR / f"{label_a}__vs__{label_b}"
    out_dir.mkdir(parents=True, exist_ok=True)
    shared = sorted(set(runs[label_a]) & set(runs[label_b]))
    key: dict[str, dict[str, str]] = {}
    for case_id in shared:
        flip = int(hashlib.sha256(case_id.encode()).hexdigest(), 16) % 2
        first, second = (label_a, label_b) if flip == 0 else (label_b, label_a)
        key[case_id] = {"Candidate A": first, "Candidate B": second}
        lines = [
            f"# {case_id}",
            "",
            "## Ground truth (learner state both candidates were judged against)",
            "```json",
            json.dumps(runs[first][case_id].get("learner_state_inputs", {}), indent=2),
            "```",
            "",
        ]
        sections_a = {s["lesson_objective_id"]: s for s in runs[first][case_id]["sections"]}
        sections_b = {s["lesson_objective_id"]: s for s in runs[second][case_id]["sections"]}
        for objective_id in sections_a:
            lines += [
                f"## Objective {objective_id}",
                "",
                "### Candidate A",
                _section_markdown(sections_a[objective_id]),
                "",
                "### Candidate B",
                _section_markdown(sections_b.get(objective_id, {})),
                "",
                "**Judgement (fill in): A / B / tie — why:**",
                "",
                "---",
                "",
            ]
        (out_dir / f"{case_id}.md").write_text("\n".join(lines))
    (out_dir / "key.json").write_text(json.dumps(key, indent=2))
    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label_a")
    parser.add_argument("label_b")
    args = parser.parse_args()
    out_dir = compare(args.label_a, args.label_b)
    print(f"wrote {out_dir} ({len(list(out_dir.glob('*.md')))} cases) — key in key.json")


if __name__ == "__main__":
    main()
