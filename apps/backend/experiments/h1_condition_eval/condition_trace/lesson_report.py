"""One document per lesson: her lesson, what each condition got, wrote, and scored.

The per-condition pages trace layers. This is the reader's view, in the order a
reader needs it: her own plan and note first, so there is something to judge the
packs against; then each condition's input and the pack it produced; then the
rubric with the judge's own words under every score.

A score with no reason beside it cannot be argued with, and the reason is the part
a supervisor reads.
"""

from __future__ import annotations

from html import escape

from app.shared.session_plan_view import SessionPlanView

from .assemble import ConditionTrace
from .render import CSS, _fields, _section_html
from .scores import DIMENSIONS, LABELS, RunScores

REPORT_CSS = (
    CSS
    + """
h1 { font-size: 19pt; }
.cond { page-break-before: always; }
.cond h2 { font-size: 13pt; text-transform: none; letter-spacing: 0; border-bottom-width: 1.6pt; }
.cond h2 .tag { font: 600 9pt "SF Mono", Menlo, monospace; color: #666; margin-left: 3mm; }
h3.part { margin-top: 5mm; font-size: 10.5pt; color: #1a1a1a; }
.sub + .sub { margin-top: 0; }
.delta-pos { color: #1a6b2f; font-weight: 600; }
.delta-neg { color: #a11; font-weight: 600; }
.delta-zero { color: #777; }
td.n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.source { page-break-before: always; }
.source pre { white-space: pre-wrap; font: 8.5pt/1.45 "SF Mono", Menlo, monospace;
  background: #fafafa; border: 0.4pt solid #e4e4e4; padding: 3mm; }
.why { margin: 2mm 0 4mm; }
.why h4 { font-size: 9.5pt; margin: 3mm 0 1mm; color: #1a1a1a; }
.why ul { margin: 0; padding-left: 5mm; }
.why li { font-size: 8.8pt; line-height: 1.45; margin-bottom: 1.2mm; }
.why li b { font: 600 8.2pt "SF Mono", Menlo, monospace; color: #555; }
"""
)


def _delta(value: float) -> str:
    klass = "delta-pos" if value > 0 else "delta-neg" if value < 0 else "delta-zero"
    return f'<span class="{klass}">{value:+.2f}</span>'


def _at(item: object, name: str) -> str:
    """Read a field whether the step models it or leaves it a plain dict.

    `activities` and `blocks` are typed on some steps and raw dicts on others, because
    the view keeps what the plan gave it. A report is not the place to care which.
    """
    value = item.get(name) if isinstance(item, dict) else getattr(item, name, None)
    return "" if value is None else str(value)


def _plan_block(plan: SessionPlanView) -> str:
    """Her lesson plan as she wrote it — the thing every condition is judged against."""
    out = ['<div class="source"><h2>Her lesson plan</h2>']
    out.append(f'<p class="sub">{escape(plan.topic or "")} — {escape(plan.subtopic or "")}</p>')
    out.append("<h3>Objectives</h3><ol>")
    for objective in plan.lesson_plan_objectives:
        out.append(f"<li>{escape(objective.objective_text or '')}</li>")
    out.append("</ol>")
    for step in plan.steps:
        out.append(f"<h3>{escape(step.title or step.step_id)}</h3>")
        if content := (step.content or "").strip():
            out.append(f"<p>{escape(content)}</p>")
        if step.activities:
            out.append("<ul>")
            for act in step.activities:
                out.append(f"<li><b>{escape(_at(act, 'who'))}</b> {escape(_at(act, 'what'))}</li>")
            out.append("</ul>")
        questions = [b for b in (step.blocks or []) if _at(b, "type") == "practice"]
        if questions:
            out.append("<ol>")
            for q in questions:
                out.append(f"<li>{escape(_at(q, 'question'))}</li>")
            out.append("</ol>")
    out.append("</div>")
    return "".join(out)


def _note_block(plan: SessionPlanView) -> str:
    """Her note, verbatim. C2 and C3 receive it; C0 and C1 never do."""
    out = ['<div class="source"><h2>Her lesson note</h2>']
    out.append(
        '<p class="sub">Verbatim, as transcribed. <b>C2 and C3 receive this; C0 and C1 '
        "never do</b> — which is the whole of what separates them.</p>"
    )
    any_note = False
    for step in plan.steps:
        note = (step.note or "").strip()
        if not note:
            continue
        any_note = True
        out.append(f"<h3>{escape(step.title or step.step_id)}</h3>")
        out.append(f"<pre>{escape(note)}</pre>")
    if not any_note:
        out.append('<p class="sub">This lesson carries no note.</p>')
    out.append("</div>")
    return "".join(out)


def _input_block(item: ConditionTrace) -> str:
    out = [
        '<h3 class="part">Input — what the model was sent</h3>',
        f'<p class="sub">Contract <span class="mono">{escape(item.contract)}</span>, declaring '
        f'<span class="mono">{escape(", ".join(item.input_fields))}</span>.</p>',
        "<h3>Lesson context — shared by every section</h3>",
        _fields(item.lesson_context),
    ]
    for index, unit in enumerate(item.units, start=1):
        out.append(
            f'<div class="unit"><h3>Objective {index} — {escape(unit.objective_text[:110])}</h3>'
        )
        out.append(_fields(unit.inputs.get("unit_context", {})))
        for key in item.input_fields:
            if key in ("lesson_context", "artefact_spec", "unit_context"):
                continue
            out.append(_fields({key: unit.inputs.get(key)}, (key,)))
        if unit.withheld:
            out.append(
                '<p class="note"><b>Withheld from this payload:</b> '
                f'<span class="mono">{escape(", ".join(unit.withheld))}</span>.</p>'
            )
        out.append("</div>")
    return "".join(out)


def _output_block(item: ConditionTrace, repeat: int) -> str:
    out = [f'<h3 class="part">Output — the pack it produced (draw {repeat})</h3>']
    for index, unit in enumerate(item.units, start=1):
        out.append(f'<div class="sec"><p class="sub">Objective {index}</p>')
        out.append(_section_html(unit.section))
        out.append("</div>")
    return "".join(out)


def _cell_means(
    scores: RunScores, lesson: str, conditions: tuple[str, ...]
) -> dict[str, dict[str, float]] | None:
    """Every condition's mean scores for a lesson, or None if any condition has none."""
    means = {c: scores.cell_mean(lesson, c) for c in conditions}
    return {c: m for c, m in means.items() if m} if all(means.values()) else None


def _results_block(lesson: str, scores: RunScores, conditions: tuple[str, ...]) -> str:
    """Every condition's mean, and the difference each rung makes over the one below it."""
    means = _cell_means(scores, lesson, conditions)
    if means is None:
        return '<p class="sub">No judged scores for this lesson in this run.</p>'
    steps = list(zip(conditions, conditions[1:], strict=False))
    head = "".join(f"<th>{c}</th>" for c in conditions)
    head += "".join(f"<th>{hi} − {lo}</th>" for lo, hi in steps)
    rows = ""
    for dim in DIMENSIONS:
        cells = "".join(f'<td class="n">{means[c][dim]:.2f}</td>' for c in conditions)
        deltas = "".join(
            f'<td class="n">{_delta(means[hi][dim] - means[lo][dim])}</td>' for lo, hi in steps
        )
        rows += f"<tr><td>{escape(LABELS[dim])}</td>{cells}{deltas}</tr>"
    draws = scores.draws_in(lesson, conditions[0])
    return (
        f'<p class="sub">Scores are 1–5. Every figure is the mean of {draws} draws rated by '
        f"{len(scores.passes)} judge pass(es) — {draws * len(scores.passes)} judgments per "
        "cell.</p>"
        f"<table><tr><th>Rubric</th>{head}</tr>{rows}</table>"
    )


def _why_block(lesson: str, scores: RunScores, conditions: tuple[str, ...]) -> str:
    """The judge's own sentence for every score above, deduplicated, by dimension."""
    out = ['<div class="why"><h3 class="part">Why the judge scored it that way</h3>']
    out.append(
        '<p class="sub">Every rationale the judge wrote for this lesson, deduplicated across '
        "draws and passes. These are its words, not a summary.</p>"
    )
    for dim in DIMENSIONS:
        line = ", ".join(
            f"{c} {m[dim]:.2f}" for c in conditions if (m := scores.cell_mean(lesson, c))
        )
        out.append(f"<h4>{escape(LABELS[dim])} — {escape(line)}</h4><ul>")
        for cond in conditions:
            for text in scores.why(lesson, cond, dim):
                out.append(f"<li><b>{cond}</b> {escape(text)}</li>")
        out.append("</ul>")
    out.append("</div>")
    return "".join(out)


def lesson_html(
    lesson: str,
    plan_title: str,
    traces: list[ConditionTrace],
    scores: RunScores | None,
    *,
    repeat: int,
    conditions: tuple[str, ...] = ("C0", "C1"),
    plan: SessionPlanView | None = None,
) -> str:
    by_code = {t.condition: t for t in traces}
    shown = tuple(c for c in conditions if c in by_code)
    body = [
        f"<h1>{escape(lesson)} — {escape(plan_title)}</h1>",
        f'<p class="sub">Run <span class="mono">{escape(scores.run if scores else "?")}</span> · '
        f"conditions {escape(', '.join(shown))} · the pack shown is draw {repeat} of each.</p>",
    ]
    if plan is not None:
        body.append(_plan_block(plan))
        body.append(_note_block(plan))
    for code in shown:
        item = by_code[code]
        body.append(
            f'<div class="cond"><h2>{code}<span class="tag">{escape(item.intent)}</span></h2>'
        )
        body.append(_input_block(item))
        body.append(_output_block(item, repeat))
        body.append("</div>")
    body.append('<div class="cond"><h2>Result — per rubric dimension</h2>')
    if scores:
        body.append(_results_block(lesson, scores, shown))
        body.append(_why_block(lesson, scores, shown))
    else:
        body.append('<p class="sub">This run has no judged scores.</p>')
    body.append("</div>")
    return f"<style>{REPORT_CSS}</style>" + "".join(body)


def scoreboard_html(
    lessons: list[str],
    plans: dict,
    scores: RunScores,
    conditions: tuple[str, ...],
) -> str:
    """Every score in one place, and nothing else.

    The per-lesson documents carry the packs and the reasoning and run to dozens of
    pages each. This is the page to put in front of someone who wants the numbers: one
    table per rubric dimension, every lesson a row, the cohort mean at the foot.
    """
    steps = list(zip(conditions, conditions[1:], strict=False))
    draws = scores.draws_in(lessons[0], conditions[0]) if lessons else 0
    body = [
        "<h1>Scores — every lesson, every condition</h1>",
        f'<p class="sub">Run <span class="mono">{escape(scores.run)}</span> · '
        f"conditions {escape(', '.join(conditions))} · {draws} draws per cell, rated by "
        f"{len(scores.passes)} judge pass(es). Scores are 1–5; every figure is the mean of "
        f"{draws * len(scores.passes)} judgments.</p>",
    ]
    for dim in DIMENSIONS:
        head = "".join(f"<th>{c}</th>" for c in conditions)
        head += "".join(f"<th>{hi} − {lo}</th>" for lo, hi in steps)
        rows = ""
        pooled: dict[str, list[float]] = {c: [] for c in conditions}
        for lesson in lessons:
            means = _cell_means(scores, lesson, conditions)
            if means is None:
                continue
            for c in conditions:
                pooled[c].append(means[c][dim])
            cells = "".join(f'<td class="n">{means[c][dim]:.2f}</td>' for c in conditions)
            deltas = "".join(
                f'<td class="n">{_delta(means[hi][dim] - means[lo][dim])}</td>' for lo, hi in steps
            )
            topic = getattr(plans.get(lesson), "topic", "") or ""
            rows += f"<tr><td>{escape(lesson)} — {escape(topic[:38])}</td>{cells}{deltas}</tr>"
        if not rows:
            continue
        mean = {c: sum(v) / len(v) for c, v in pooled.items() if v}
        cells = "".join(f'<td class="n"><b>{mean[c]:.2f}</b></td>' for c in conditions)
        deltas = "".join(f'<td class="n">{_delta(mean[hi] - mean[lo])}</td>' for lo, hi in steps)
        rows += f"<tr><td><b>All six pooled</b></td>{cells}{deltas}</tr>"
        body.append(f"<h2>{escape(LABELS[dim])}</h2>")
        body.append(f"<table><tr><th>Lesson</th>{head}</tr>{rows}</table>")
    return f"<style>{REPORT_CSS}</style>" + "".join(body)
