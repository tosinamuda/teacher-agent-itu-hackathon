"""Turn a labelled run into blinded rater packets.

One directory per lesson holding the four packs as anonymous candidates, the
lesson reference every rater reads first, and the key that de-anonymises them.
Candidate order is derived from the lesson and run label, never sampled, so a
packet can be rebuilt byte-identically from the run alone.

Raters see the teacher's plan AND her note (the reference): fidelity to what she
taught is the thing being judged, and it cannot be judged blind to it.

    uv run python -m experiments.h1_condition_eval.packets h1-ea245a9e96
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from experiments.h1_condition_eval.config import RUNS_DIR
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

LETTERS = "ABCDEFGH"

# A TikZ figure and any centring wrapper around it.
_TIKZ_BLOCK = re.compile(
    r"(?:\\begin\{center\}\s*)?\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}"
    r"(?:\s*\\end\{center\})?",
    re.DOTALL,
)


def _blind_order(label: str, lesson: str, conditions: list[str]) -> list[str]:
    """A fixed shuffle of the conditions — reproducible, and different per lesson."""
    return sorted(
        conditions, key=lambda code: hashlib.sha256(f"{label}|{lesson}|{code}".encode()).hexdigest()
    )


def _render_pack(sections: list[dict[str, Any]], letter: str) -> str:
    lines = [f"# Candidate {letter}", ""]
    for section in sections:
        lines += [f"## {section['title']}", ""]
        for block in section["blocks"]:
            text = (block.get("text") or "").strip()
            caption = (block.get("caption") or "").strip()
            label = (block.get("figure_ref") or "").strip()
            if text:
                lines += [text, ""]
            elif block.get("block_type") == "visual" or caption or label:
                # Keep the note's own label: prose cites "(see fig-08)", so a
                # rendered figure without its label reads as a different, missing
                # drawing.
                name = f"figure {label}" if label else "figure"
                lines += [f"*[{name}: {caption}]*".replace(": ]", "]"), ""]
    return "\n".join(lines).rstrip() + "\n"


def _readable(value: str) -> str:
    """Note prose with figure SOURCE dropped.

    Some notes carry their diagrams as TikZ. A rater reading the lesson gains
    nothing from forty lines of ``\\draw`` commands, and each figure is already
    described in the prose immediately above it.
    """
    without_figures = _TIKZ_BLOCK.sub("", value)
    return "\n".join(line for line in without_figures.splitlines() if line.strip()).strip()


def _render_step(step: dict[str, Any]) -> list[str]:
    lines = [f"### {step['title']}", ""]
    activities = step.get("activities") or []
    if activities:
        lines.append("**Activities, in order:**")
        lines += [f"- *{item['who']}* — {item['what']}" for item in activities]
        lines.append("")
    # Her note verbatim (the model's evidence), TikZ dropped for the rater's eyes only —
    # each figure's written description sits above its code and carries the meaning.
    note = _readable(step.get("note") or "")
    if note:
        lines += [note, ""]
        return lines
    for block in step.get("blocks") or []:
        for key in ("content", "problem", "question", "final_answer"):
            value = _readable(block.get(key) or "")
            if value:
                lines += [value, ""]
        for entry in block.get("steps") or []:
            value = _readable(entry.get("content") or "")
            if value:
                lines += [value, ""]
    return lines


def _render_reference(plan: dict[str, Any]) -> str:
    lines = [
        f"# Lesson reference — {plan.get('topic') or ''}".rstrip(),
        "",
        f"**Subject** {plan.get('subject')} · **Grade** {plan.get('grade')} · "
        f"**Week** {plan.get('week')}",
        f"**Subtopic** {plan.get('subtopic') or ''}".rstrip(),
        "",
        "## Lesson objectives",
        "",
    ]
    for index, objective in enumerate(plan.get("lesson_plan_objectives") or [], start=1):
        lines.append(f"{index}. {objective['objective_text']}")
    lines += ["", "## The lesson as taught", ""]
    for step in plan.get("steps") or []:
        if step.get("step_kind") == "core":
            lines += _render_step(step)
    return "\n".join(lines).rstrip() + "\n"


def build(label: str, out_dir: Path) -> int:
    run = json.loads((RUNS_DIR / label / "run.json").read_text())
    plans = {
        case["lesson"]: case["plan"] for case in json.loads(EVAL_SET_PATH.read_text())["cases"]
    }
    by_lesson: dict[str, dict[str, Any]] = {}
    for row in run["cases"]:
        by_lesson.setdefault(row["lesson"], {})[row["condition"]] = row

    for lesson, rows in by_lesson.items():
        order = _blind_order(label, lesson, sorted(rows))
        lesson_dir = out_dir / lesson
        lesson_dir.mkdir(parents=True, exist_ok=True)
        key = {}
        for letter, code in zip(LETTERS, order, strict=False):
            (lesson_dir / f"candidate-{letter}.md").write_text(
                _render_pack(rows[code]["sections_json"], letter), encoding="utf-8"
            )
            key[letter] = code
        (lesson_dir / "KEY.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
        (lesson_dir / "REFERENCE.md").write_text(_render_reference(plans[lesson]), encoding="utf-8")
        print(f"  {lesson}: {' '.join(f'{k}={v}' for k, v in key.items())}")
    print(f"wrote {len(by_lesson)} packets to {out_dir}")
    return 0


def build_arms(arms: dict[str, str], condition: str, out_dir: Path) -> int:
    """Blind one condition ACROSS runs, so arms are compared like for like.

    ``build`` blinds the conditions inside a single run; an arm comparison holds
    the condition fixed and varies the run that produced it.
    """
    plans = {
        case["lesson"]: case["plan"] for case in json.loads(EVAL_SET_PATH.read_text())["cases"]
    }
    by_lesson: dict[str, dict[str, Any]] = {}
    for arm, label in arms.items():
        run = json.loads((RUNS_DIR / label / "run.json").read_text())
        for row in run["cases"]:
            if row["condition"] == condition:
                by_lesson.setdefault(row["lesson"], {})[arm] = row

    # Hashing balances poorly over few candidates — it put one arm first on 4 of
    # 5 lessons, so any position bias would read as that arm winning. Rotate by
    # lesson instead: still derived from the run alone, but counterbalanced.
    for index, (lesson, rows) in enumerate(sorted(by_lesson.items())):
        names = sorted(rows)
        order = names[index % len(names) :] + names[: index % len(names)]
        lesson_dir = out_dir / lesson
        lesson_dir.mkdir(parents=True, exist_ok=True)
        key = {}
        for letter, arm in zip(LETTERS, order, strict=False):
            (lesson_dir / f"candidate-{letter}.md").write_text(
                _render_pack(rows[arm]["sections_json"], letter), encoding="utf-8"
            )
            key[letter] = f"{arm}-{condition}"
        (lesson_dir / "KEY.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
        (lesson_dir / "REFERENCE.md").write_text(_render_reference(plans[lesson]), encoding="utf-8")
        print(f"  {lesson}: {' '.join(f'{k}={v}' for k, v in key.items())}")
    print(f"wrote {len(by_lesson)} packets to {out_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label", nargs="?", help="run label under runs/")
    parser.add_argument("--out", type=Path, required=True, help="directory to write packets into")
    parser.add_argument(
        "--arms", nargs="*", help="arm=label pairs to compare at one condition", default=None
    )
    parser.add_argument("--condition", default="C3", help="condition to hold fixed across arms")
    args = parser.parse_args()
    if args.arms:
        arms = dict(pair.split("=", 1) for pair in args.arms)
        return build_arms(arms, args.condition, args.out)
    if not args.label:
        raise SystemExit("give a run label, or --arms arm=label ... to compare arms")
    return build(args.label, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
