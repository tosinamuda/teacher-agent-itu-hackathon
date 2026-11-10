"""Render the saved bake-off cells to a printable HTML report (LaTeX tables + figures shown).

    cd apps/backend
    uv run python -m experiments.sequencing_bakeoff.render_pdf   # writes report.html

Markdown is rendered by marked.js and math by MathJax (both CDN, mirroring the frontend), so
the tables render as tables and figures as images. A separate Chrome `--print-to-pdf` step
turns report.html into report.pdf. For human inspection — the LLM judges are not trusted.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import cast

from app.shared.json_types import JsonObject

_OUT = Path(__file__).resolve().parents[2] / ".diagnostics" / "sequencing-bakeoff"
_RUNS = _OUT / "scale_runs.json"
_HTML = _OUT / "report.html"

_VARIANT_ORDER = ["regenerate", "markers", "blocklist", "append"]
_VARIANT_LABEL = {
    "regenerate": "V0 REGENERATE (LLM writes everything)",
    "markers": "V1 MARKERS (inline {{asset}} tokens)",
    "blocklist": "V2 BLOCKLIST (ordered prose/ref blocks)",
    "append": "V3 APPEND (prose only, assets dumped after)",
}
_TOPIC_TITLE = {
    "ch01-b035": "Topic: a million (powers-of-ten table + counting charts)",
    "ch01-b017": "Topic: decimal place values (place-value table + figures)",
    "ch04-b018": "Topic: improper equivalent fractions (figures only)",
}

_PAGE = r"""<!doctype html>
<html><head><meta charset="utf-8"><title>Sequencing bake-off — generated content</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'],['\\(','\\)']], displayMath: [['$$','$$'],['\\[','\\]']] },
  svg: { fontCache: 'global' }
};
</script>
<style>
  body { font: 15px/1.5 -apple-system, Segoe UI, Roboto, sans-serif; color: #1a1a1a;
         max-width: 820px; margin: 0 auto; padding: 24px; }
  h1.topic { border-top: 3px solid #c44; padding-top: 16px; page-break-before: always; }
  h1.topic:first-of-type { page-break-before: avoid; }
  .cell { border: 1px solid #ddd; border-radius: 8px; padding: 14px 18px; margin: 14px 0;
          page-break-inside: avoid; }
  .meta { font: 12px ui-monospace, monospace; color: #555; background: #f6f6f6;
          padding: 6px 10px; border-radius: 6px; margin-bottom: 10px; }
  .meta .bad { color: #c00; font-weight: 700; }
  h2.variant { margin: 6px 0; font-size: 16px; }
  figure { margin: 12px 0; text-align: center; }
  figure img { max-width: 60%; border: 1px solid #eee; border-radius: 6px; }
  figcaption { font: 11px monospace; color: #888; }
  table { border-collapse: collapse; }
  .prose :is(table) td, .prose :is(table) th { border: 1px solid #ccc; padding: 2px 8px; }
  .lead { color:#444; }
</style></head><body>
<h1>Sequencing bake-off — generated lesson-step content</h1>
<p class="lead">3 topics x 4 variants x 3 seeds. Each card shows the actual generated step
(tables + figures rendered). Metrics line carries the deterministic flags and both judge means
so you can correlate content with score. Judge the content yourself — the LLM judges showed
verbosity bias (and one saturated at 5/5).</p>
__BODY__
<script>
  (function () {
    function render() {
      document.querySelectorAll('.prose').forEach(function (div) {
        var math = [];
        var md = div.textContent;
        var prot = md.replace(/\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$[^\n$]+?\$/g,
          function (m) { math.push(m); return '@@M' + (math.length - 1) + '@@'; });
        var out = marked.parse(prot);
        out = out.replace(/@@M(\d+)@@/g, function (_, i) { return math[+i]; });
        div.innerHTML = out;
      });
    }
    render();
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
    document.body.appendChild(s);
  })();
</script>
</body></html>
"""


def _render_block(block: JsonObject) -> str:
    if str(block.get("type")) == "visual" and block.get("url"):
        src = html.escape(str(block["url"]))
        # show the real caption (the transcluded figcaption), falling back to the record id
        cap = html.escape(str(block.get("caption") or block.get("source_record_id") or "figure"))
        return f'<figure><img src="{src}" loading="eager"><figcaption>{cap}</figcaption></figure>'
    content = str(block.get("content") or "")
    return f'<div class="prose">{html.escape(content)}</div>'


def _cell_block_list(step: JsonObject) -> list[JsonObject]:
    raw = step.get("blocks")
    if not isinstance(raw, list):
        return []
    return [cast(JsonObject, b) for b in raw if isinstance(b, dict)]


def _meta_line(cell: JsonObject) -> str:
    metrics = cast(JsonObject, cell.get("metrics") or {})
    judges = cast(JsonObject, cell.get("judges") or {})
    valid = metrics.get("latex_valid")
    valid_html = "latex VALID" if valid else '<span class="bad">latex INVALID</span>'
    halluc = metrics.get("refs_hallucinated") or []
    missed = metrics.get("refs_missed") or []
    if not halluc and not missed:
        refs = "refs clean"
    else:
        refs = f'<span class="bad">refs miss={missed} halluc={halluc}</span>'
    judge_bits = []
    for name, score in judges.items():
        if isinstance(score, dict) and "mean" in score:
            judge_bits.append(f"{name.split('/')[-1]}={score['mean']}")
    fidelity = cell.get("fidelity_violations")
    fidelity_html = ""
    if isinstance(fidelity, list):
        count = len(fidelity)
        fidelity_html = (
            " | fidelity clean"
            if count == 0
            else f' | <span class="bad">fidelity {count} violation(s)</span>'
        )
    return (
        f"seed {cell.get('seed')} | {valid_html} | llm_chars={metrics.get('llm_authored_chars')} | "
        f"{refs} | judges {' '.join(judge_bits)}{fidelity_html}"
    )


def main() -> None:
    runs = json.loads(_RUNS.read_text(encoding="utf-8"))
    by_topic: dict[str, list[JsonObject]] = {}
    for cell in runs:
        by_topic.setdefault(str(cell.get("topic")), []).append(cell)

    body: list[str] = []
    for topic, cells in by_topic.items():
        body.append(f'<h1 class="topic">{html.escape(_TOPIC_TITLE.get(topic, topic))}</h1>')
        for variant in _VARIANT_ORDER:
            vcells = sorted(
                (c for c in cells if c.get("variant") == variant),
                key=lambda c: c.get("seed", 0),
            )
            for cell in vcells:
                if cell.get("error"):
                    continue
                step = cast(JsonObject, cell["step"])
                blocks = "".join(_render_block(b) for b in _cell_block_list(step))
                body.append(
                    f'<div class="cell"><h2 class="variant">{_VARIANT_LABEL[variant]}</h2>'
                    f'<div class="meta">{_meta_line(cell)}</div>{blocks}</div>'
                )

    _HTML.write_text(_PAGE.replace("__BODY__", "\n".join(body)), encoding="utf-8")
    print(f"wrote {_HTML}")
    print("Next: print to PDF with headless Chrome (see render_pdf docstring / runner).")


if __name__ == "__main__":
    main()
