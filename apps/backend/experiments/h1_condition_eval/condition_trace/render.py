"""Render one condition's input and output to a page a reader can audit.

Deliberately literal about the input: the payload is shown exactly as the contract
carries it, expanded field by field, and every unit field the contract left out is
named underneath. Showing only what was sent makes an absent layer indistinguishable
from one that arrived empty, and telling those two apart is the whole point of the
document.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

from app.domains.evaluation.application.worksheet_html.renderer import html_to_pdf

from .assemble import ConditionTrace
from .layers import INPUT_LAYERS, LayerTrace, trace

CSS = """
@page { size: A4; margin: 16mm 14mm; @bottom-right { content: counter(page);
  font: 8pt/1 -apple-system, sans-serif; color: #999; } }
* { box-sizing: border-box; }
body { font: 9.5pt/1.5 -apple-system, "Helvetica Neue", sans-serif; color: #1a1a1a; margin: 0; }
h1 { font-size: 17pt; margin: 0 0 2mm; letter-spacing: -0.2px; }
h2 { font-size: 11pt; margin: 7mm 0 2.5mm; padding-bottom: 1.2mm;
     border-bottom: 1.2pt solid #1a1a1a; text-transform: uppercase; letter-spacing: 0.8px; }
h3 { font-size: 9.5pt; margin: 4mm 0 1.5mm; color: #333; }
.sub { color: #666; font-size: 9pt; margin: 0 0 1mm; }
.intent { background: #f4f4f2; border-left: 2.5pt solid #666; padding: 2.5mm 3mm;
          margin: 3mm 0; font-size: 9pt; }
table { width: 100%; border-collapse: collapse; margin: 2mm 0 3mm; font-size: 8.5pt; }
th { text-align: left; font-weight: 600; border-bottom: 0.8pt solid #1a1a1a;
     padding: 1.4mm 2mm 1.4mm 0; }
td { padding: 1.4mm 2mm 1.4mm 0; border-bottom: 0.4pt solid #e0e0e0; vertical-align: top; }
td.n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.yes { color: #1a6b2f; font-weight: 600; }
.no  { color: #999; }
.warn { color: #a8560c; font-weight: 600; }
.bad { color: #a11; font-weight: 600; }
.field { margin: 0 0 2.5mm; }
.field .k { font: 600 8pt "SF Mono", Menlo, monospace; color: #444; }
.field .v { white-space: pre-wrap; word-wrap: break-word; font-size: 8.5pt;
            background: #fafaf8; border: 0.4pt solid #e2e2de; border-radius: 1.5pt;
            padding: 2mm 2.5mm; margin-top: 1mm; }
.field .v.empty { color: #a00; background: #fff6f6; border-color: #f0d8d8; font-style: italic; }
.mono { font-family: "SF Mono", Menlo, monospace; font-size: 8pt; }
.unit { page-break-inside: avoid; margin: 0 0 5mm; padding-top: 2mm; }
.unit + .unit { border-top: 0.4pt dashed #ccc; }
.sec { page-break-inside: avoid; margin: 0 0 4mm; }
.blk { margin: 1.5mm 0; padding-left: 3mm; border-left: 2pt solid #ddd; }
.blk .t { font: 600 7.5pt "SF Mono", Menlo, monospace; color: #777;
          text-transform: uppercase; letter-spacing: 0.5px; }
.blk .x { white-space: pre-wrap; font-size: 8.5pt; }
.pr { margin: 1.2mm 0; font-size: 8.5pt; }
.pr .q { }
.pr .a { color: #1a6b2f; padding-left: 4mm; }
.brk { page-break-before: always; }
.note { font-size: 8.5pt; color: #555; margin: 1.5mm 0 0; }
"""

VERDICT_CLASS = {"grounded": "yes", "substituted": "warn", "unsourced": "bad", "absent": "no"}
VERDICT_WORD = {
    "grounded": "grounded",
    "substituted": "substituted",
    "unsourced": "unsourced",
    "absent": "not produced",
}


def _value(value: object) -> str:
    if value in (None, "", [], {}):
        return '<div class="v empty">empty — the condition supplies nothing here</div>'
    if isinstance(value, str):
        return f'<div class="v">{escape(value)}</div>'
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return '<div class="v">' + escape("\n".join(f"• {v}" for v in value)) + "</div>"
    text = json.dumps(value, indent=1, ensure_ascii=False, default=str)
    return f'<div class="v mono">{escape(text)}</div>'


def _fields(payload: dict, keys: tuple[str, ...] = ()) -> str:
    names = keys or tuple(payload)
    return "".join(
        f'<div class="field"><span class="k">{escape(k)}</span>{_value(payload.get(k))}</div>'
        for k in names
    )


def _input_layer_table(view: dict) -> str:
    rows = ""
    for layer in INPUT_LAYERS:
        here = layer.present_in(view)
        rows += (
            f"<tr><td>{escape(layer.name)}</td><td>{escape(layer.carries)}</td>"
            f'<td class="sub">{escape(layer.channel)}</td>'
            f'<td class="{"yes" if here else "no"}">{"present" if here else "absent"}</td></tr>'
        )
    return (
        "<table><tr><th>Input layer</th><th>What it carries</th><th>Channel</th>"
        f"<th>In this condition</th></tr>{rows}</table>"
    )


def _trace_table(traces: list[LayerTrace]) -> str:
    rows = ""
    for item in traces:
        verdict = item.verdict
        note = ""
        if verdict == "substituted" and item.layer.substitute_note:
            note = f'<div class="note">{escape(item.layer.substitute_note)}</div>'
        rows += (
            f"<tr><td>{escape(item.layer.name)}<br>"
            f'<span class="sub">{escape(item.layer.is_what)}</span></td>'
            f'<td class="n">{item.produced}</td>'
            f"<td>{escape(item.sourced_by)}{note}</td>"
            f'<td class="{VERDICT_CLASS[verdict]}">{VERDICT_WORD[verdict]}</td></tr>'
        )
    return (
        "<table><tr><th>Output layer</th><th>Made</th><th>Written from</th>"
        f"<th>Verdict</th></tr>{rows}</table>"
    )


def _section_html(section: dict) -> str:
    if not section:
        return '<p class="sub">No section was produced for this objective.</p>'
    out = f"<h3>{escape(str(section.get('title') or 'untitled'))}</h3>"
    for block in section.get("blocks") or []:
        kind = str(block.get("block_type") or "block")
        text = str(block.get("text") or block.get("source_tikz") or "").strip()
        out += (
            f'<div class="blk"><div class="t">{escape(kind)}</div>'
            f'<div class="x">{escape(text)}</div></div>'
        )
    for index, item in enumerate(section.get("practice") or [], start=1):
        out += (
            f'<div class="pr"><div class="q"><b>{index}.</b> '
            f"{escape(str(item.get('prompt') or ''))}</div>"
            f'<div class="a">answer: {escape(str(item.get("answer") or ""))}</div></div>'
        )
    return out


def condition_html(item: ConditionTrace, plan_title: str) -> str:
    first = item.units[0].probe_view if item.units else {}
    body = [
        f"<h1>{escape(item.lesson)} — condition {escape(item.condition)}</h1>",
        f'<p class="sub">{escape(plan_title)}</p>',
        f'<div class="intent">{escape(item.intent)}</div>',
        "<h2>Input layers</h2>",
        _input_layer_table(first),
        "<h2>What the model is sent</h2>",
        f'<p class="sub">Contract <span class="mono">{escape(item.contract)}</span>, '
        f'declaring: <span class="mono">{escape(", ".join(item.input_fields))}</span>.</p>',
        "<h3>Lesson context — shared by every section</h3>",
        _fields(item.lesson_context),
    ]
    for index, unit in enumerate(item.units, start=1):
        body.append(
            f'<div class="unit"><h3>Objective {index} — {escape(unit.objective_text[:110])}</h3>'
        )
        body.append(_fields(unit.inputs.get("unit_context", {})))
        for key in item.input_fields:
            if key in ("lesson_context", "artefact_spec", "unit_context"):
                continue
            body.append(_fields({key: unit.inputs.get(key)}, (key,)))
        if unit.withheld:
            body.append(
                '<p class="note"><b>Withheld from this payload:</b> '
                f'<span class="mono">{escape(", ".join(unit.withheld))}</span> — '
                "carried by the plan or the unit, not sent under this condition.</p>"
            )
        body.append("</div>")
    body.append('<h2 class="brk">What the model produced</h2>')
    for index, unit in enumerate(item.units, start=1):
        body.append(f'<div class="sec"><p class="sub">Objective {index}</p>')
        body.append(_section_html(unit.section))
        body.append("</div>")
    body.append("<h2>Layer by layer: what was grounded and what was not</h2>")
    body.append(_trace_table(trace(first, item.sections)))
    return f"<style>{CSS}</style>" + "".join(body)


def to_pdf(html: str, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(html_to_pdf(html))
    return path
