"""The cross-lesson view: which layers the design grounds, and which it cannot.

The per-condition pages show one lesson at a time, where a gap can always be read
as a property of that lesson. This aggregates over the cohort so the distinction
between "this teacher wrote little down" and "the condition never carries this
kind of content" becomes visible, because only the second is a fact about the
treatment.
"""

from __future__ import annotations

from collections import Counter
from html import escape

from .assemble import CONDITION_INTENT, ConditionTrace
from .layers import INPUT_LAYERS, OUTPUT_LAYERS, trace
from .render import CSS, VERDICT_CLASS, VERDICT_WORD

CONDITIONS = ("C0", "C1", "C2", "C3")


def _verdicts(traces: list[ConditionTrace]) -> dict[tuple[str, str], Counter]:
    tally: dict[tuple[str, str], Counter] = {}
    for item in traces:
        if not item.units:
            continue
        for layer_trace in trace(item.units[0].probe_view, item.sections):
            key = (layer_trace.layer.key, item.condition)
            tally.setdefault(key, Counter())[layer_trace.verdict] += 1
    return tally


def _availability(traces: list[ConditionTrace]) -> dict[tuple[str, str], tuple[int, int]]:
    tally: dict[tuple[str, str], list[int]] = {}
    for item in traces:
        for unit in item.units:
            for layer in INPUT_LAYERS:
                slot = tally.setdefault((layer.key, item.condition), [0, 0])
                slot[1] += 1
                slot[0] += layer.present_in(unit.probe_view)
    return {key: (hit, total) for key, (hit, total) in tally.items()}


def _cell(counts: Counter) -> str:
    if not counts:
        return '<td class="no">—</td>'
    verdict, count = counts.most_common(1)[0]
    total = sum(counts.values())
    share = f"{count}/{total}"
    return f'<td class="{VERDICT_CLASS[verdict]}">{VERDICT_WORD[verdict]}<br>{share}</td>'


def summary_html(traces: list[ConditionTrace], lessons: int) -> str:
    verdicts = _verdicts(traces)
    availability = _availability(traces)

    grounding = "".join(
        f"<tr><td>{escape(layer.name)}<br><span class='sub'>{escape(layer.is_what)}</span></td>"
        + "".join(_cell(verdicts.get((layer.key, code), Counter())) for code in CONDITIONS)
        + "</tr>"
        for layer in OUTPUT_LAYERS
    )

    supply = ""
    for layer in INPUT_LAYERS:
        cells = ""
        for code in CONDITIONS:
            hit, total = availability.get((layer.key, code), (0, 0))
            if not total:
                cells += '<td class="no">—</td>'
                continue
            klass = "yes" if hit == total else "no" if hit == 0 else "warn"
            cells += f'<td class="{klass}">{hit}/{total}</td>'
        supply += (
            f"<tr><td>{escape(layer.name)}<br>"
            f"<span class='sub'>{escape(layer.carries)} &middot; {escape(layer.channel)}</span>"
            f"</td>{cells}</tr>"
        )

    heads = "".join(f"<th>{code}</th>" for code in CONDITIONS)
    intents = "".join(
        f"<tr><td class='mono'>{code}</td><td>{escape(CONDITION_INTENT[code])}</td></tr>"
        for code in CONDITIONS
    )

    return f"""<style>{CSS}</style>
<h1>What each condition supplies, and what the pack is built from</h1>
<p class="sub">{lessons} lessons &middot; four conditions &middot; one draw each,
from the <span class="mono">clean-six</span> run.</p>

<div class="intent">A pack has layers, and they are not interchangeable. An
explanation, a worked example and a practice question each need a different kind of
input to be written <em>from the lesson</em> rather than from what the model already
knows about the topic. This traces each layer of the output back to the input layer
that could have supplied it.</div>

<h2>The conditions</h2>
<table><tr><th>Condition</th><th>What it adds</th></tr>{intents}</table>

<h2>Input supply — units where the layer arrives filled</h2>
<table><tr><th>Input layer</th>{heads}</tr>{supply}</table>

<h2>Output grounding — where each layer of the pack comes from</h2>
<table><tr><th>Output layer</th>{heads}</tr>{grounding}</table>
<p class="note"><span class="yes">grounded</span> the input layer that should
supply it is present &middot; <span class="warn">substituted</span> it is absent
and a different layer stood in &middot; <span class="bad">unsourced</span> nothing
in the input supplies it, so the model wrote it from its own knowledge.</p>
"""
