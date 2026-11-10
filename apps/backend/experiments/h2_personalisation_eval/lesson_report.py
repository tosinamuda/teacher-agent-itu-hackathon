"""P0 against P1 for one learner, on a page a reader can audit.

The H1 trace answers "what did the condition receive, and what did it write". This
answers the H2 question, which is narrower and harder to see in a score table: the two
packs are the SAME artefact until the personaliser touches it, so a reader needs the
learner's record and both packs together to judge whether the difference earned itself.

Shows, in order: the learner's marked classwork, the state derived from it EXACTLY as
the prompt carries it, then P0 and P1 section by section, then the judge's scores with
every rationale.

    uv run python -m experiments.h2_personalisation_eval.lesson_report \\
        --run h2-gptoss-fixed --lesson t3-w05 --student student-01
"""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    prompt_state,
)
from app.domains.evaluation.application.worksheet_html.renderer import html_to_pdf
from experiments.h1_condition_eval.condition_trace.render import CSS, _section_html
from experiments.h2_personalisation_eval.analysis import _cell, _load
from experiments.h2_personalisation_eval.learner_states import states_for
from experiments.h2_personalisation_eval.rating import DIMENSIONS, RUNS
from experiments.h2_personalisation_eval.students import load

EXTRA_CSS = """
.pane{border:1px solid #d8d8d8;border-radius:4px;padding:10px 12px;margin:10px 0}
.p0{border-left:4px solid #999}
.p1{border-left:4px solid #2a6}
.ev{background:#fafafa;border:1px solid #eee;padding:8px 10px;margin:6px 0;font-size:9pt}
.ev .q{font-weight:600}
.ev .w{font-family:ui-monospace,Menlo,monospace;white-space:pre-wrap}
.mis{color:#a33}
table.sc{border-collapse:collapse;width:100%;font-size:9pt;margin:8px 0}
table.sc th,table.sc td{border:1px solid #ddd;padding:4px 6px;text-align:left}
table.sc td.n{text-align:right}
"""


def _classwork_block(classwork, student) -> str:
    """The learner's marked script — the evidence everything downstream rests on."""
    rows = [
        "<table class='sc'><tr><th>Q</th><th>question</th><th>mark</th>"
        "<th>the learner wrote</th><th>coded misconception</th></tr>"
    ]
    for response in sorted(student.responses, key=lambda r: r.n):
        question = classwork.questions[response.n]
        misconception = (
            f"{response.misconception_code} — {response.misconception_why}"
            if response.misconception_code
            else ""
        )
        rows.append(
            f"<tr><td class='n'>{response.n}</td><td>{escape(question.text)}</td>"
            f"<td>{escape(response.mark)}</td>"
            f"<td class='ev w'>{escape(response.working or '')}</td>"
            f"<td class='mis'>{escape(misconception)}</td></tr>"
        )
    return (
        f"<h2>The learner's marked classwork</h2>"
        f"<p class='sub'>{escape(student.id)} · teacher's total "
        f"{escape(student.teacher_total)} · assessed set: "
        f"{escape(classwork.assessed_set)}</p>" + "".join(rows) + "</table>"
    )


def _state_block(states: dict) -> str:
    """The state as the PROMPT carries it — not the model, the projection of it."""
    out = [
        "<h2>The learner state, exactly as the personaliser receives it</h2>",
        "<p class='sub'>This is the projection the prompt carries, not the schema. "
        "An objective with no marked evidence gets no state, and its section is passed "
        "through unchanged.</p>",
    ]
    for objective, state in sorted(states.items()):
        payload = json.dumps(prompt_state(state), indent=1, ensure_ascii=False)
        out.append(
            f"<div class='pane'><b>{escape(objective)}</b>"
            f"<div class='ev w'>{escape(payload)}</div></div>"
        )
    return "".join(out)


def _packs_block(p0: list[dict], p1: list[dict], outcomes: list[dict]) -> str:
    by_outcome = {str(o.get("section_id") or o.get("lesson_objective_id")): o for o in outcomes}
    out = ["<h2>The two packs, section by section</h2>"]
    for index, base in enumerate(p0):
        personalised = p1[index] if index < len(p1) else {}
        key = str(base.get("section_id") or "")
        outcome = by_outcome.get(key, {})
        verdict = str(outcome.get("outcome") or "—")
        out.append(
            f"<h3>{escape(key or f'section {index + 1}')} · personalisation: "
            f"<code>{escape(verdict)}</code></h3>"
            f"<div class='pane p0'><b>P0 — the base pack, unchanged</b>"
            f"{_section_html(base)}</div>"
            f"<div class='pane p1'><b>P1 — personalised for this learner</b>"
            f"{_section_html(personalised)}</div>"
        )
    return "".join(out)


def _scores_block(run_label: str, lesson: str, student: str) -> str:
    try:
        key, by_candidate = _load(run_label)
    except FileNotFoundError:
        return "<h2>Judgments</h2><p class='sub'>This run is not rated.</p>"
    mine = {
        row["condition"]: by_candidate.get(row["candidate_id"], [])
        for row in key
        if row["lesson"] == lesson and row["student"] == student
    }
    if not mine:
        return "<h2>Judgments</h2><p class='sub'>This learner is not in the rating key.</p>"
    rows = ["<table class='sc'><tr><th>rubric</th><th>P0</th><th>P1</th><th>P1 − P0</th></tr>"]
    reasons = []
    for dimension in DIMENSIONS:
        zero, why0 = _cell(mine.get("P0", []), dimension)
        one, why1 = _cell(mine.get("P1", []), dimension)
        delta = "—" if zero is None or one is None else f"{one - zero:+.2f}"
        rows.append(
            f"<tr><td>{escape(dimension)}</td>"
            f"<td class='n'>{'—' if zero is None else f'{zero:.2f}'}</td>"
            f"<td class='n'>{'—' if one is None else f'{one:.2f}'}</td>"
            f"<td class='n'><b>{delta}</b></td></tr>"
        )
        for label, texts in (("P0", why0), ("P1", why1)):
            for text in texts:
                reasons.append(
                    f"<div class='ev'><span class='q'>{escape(dimension)} · {label}</span> "
                    f"— {escape(text)}</div>"
                )
    return (
        "<h2>What the judge said</h2>"
        + "".join(rows)
        + "</table><h3>Every rationale</h3>"
        + "".join(reasons)
    )


def report_html(run_label: str, lesson: str, student_id: str) -> str:
    run = json.loads((RUNS / run_label / "run.json").read_text())
    cases = {
        c["condition"]: c
        for c in run["cases"]
        if c["lesson"] == lesson and c["student"] == student_id
    }
    if "P0" not in cases or "P1" not in cases:
        raise SystemExit(f"{run_label}: no P0/P1 pair for {lesson} {student_id}")
    classwork = load(lesson)
    student = next(s for s in classwork.students if s.id == student_id)
    body = [
        f"<h1>{escape(lesson)} · {escape(student_id)} — P0 against P1</h1>",
        f"<p class='sub'>Run <b>{escape(run_label)}</b> · personaliser "
        f"{escape(str(run['model']))} · base pack "
        f"{escape(json.dumps(run['base']))}</p>",
        _classwork_block(classwork, student),
        _state_block(states_for(classwork, student)),
        _packs_block(
            cases["P0"]["sections"],
            cases["P1"]["sections"],
            cases["P1"].get("personalisation") or [],
        ),
        _scores_block(run_label, lesson, student_id),
    ]
    return f"<style>{CSS}{EXTRA_CSS}</style>" + "".join(body)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    parser.add_argument("--lesson", required=True)
    parser.add_argument("--student", required=True)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    path = args.out or RUNS / args.run / f"{args.lesson}-{args.student}.pdf"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(html_to_pdf(report_html(args.run, args.lesson, args.student)))
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
