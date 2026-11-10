/**
 * Strip textbook source citations from reading-note prose.
 *
 * Mirrors the backend's reading-note text cleaning (in
 * `apps/backend/src/app/domains/evaluation/application/worksheet_html/renderer.py` —
 * `_EDITORIAL_SOURCES_RE` plus `_strip_source_citations`, both applied in
 * `_render_markdown`) so the same content rendered as a PDF on the backend and
 * as HTML in the browser presents identically to students and raters.
 *
 * H1/H2 raters judge fit-to-objective, not source grounding (that lives in the
 * separate source-grounding audit pack). Three shapes are removed:
 *   1. Parenthesised `(Source: …)` annotations — the editorial "(Source: REF-1
 *      for X)" meta-commentary the model appends, the contentless `(Source:)`
 *      it sometimes leaves, and any `(Source: <text>)` in between. Removed first
 *      so stripping the inner `REF-N` never leaves a mangled `(Source: for X)`
 *      fragment. Mirrors the backend `_EDITORIAL_SOURCES_RE`.
 *   2. Whole `Sources: …` lines — the trailing citation footer most blocks end
 *      with — including an optional leading/trailing markdown emphasis `_`.
 *   3. Inline citation markers — `(REF-1)`, `[REF-1]`, `⟦REF-1⟧`, `【REF-1】`,
 *      and bare `REF-1` — wherever they appear mid-prose.
 *
 * After removal, runs of spaces from a cut are collapsed and space-before-punct
 * is tidied so the surrounding prose still reads naturally.
 */
// Any parenthesised `(Source: …)` / `(Sources: …)` annotation, content or not.
// `[^()]*` stops at the first paren so it never swallows surrounding text.
const EDITORIAL_SOURCES_RE = /\s*\(\s*sources?\s*:[^()]*\)/gi;
const SOURCES_LINE_RE = /^[ \t]*_?\s*sources?\s*:.*?_?[ \t]*$/gim;
const INLINE_CITATION_RE =
  /\s*(?:\(\s*REF-\d+\s*\)|\[\s*REF-\d+\s*\]|⟦\s*REF-\d+\s*⟧|【\s*REF-\d+\s*】|\bREF-\d+\b)/gi;
const SPACE_BEFORE_PUNCT_RE = /[ \t]+([,.;:!?])/g;
const MULTISPACE_RE = /[ \t]{2,}/g;

/**
 * Remove textbook source citations from H1/H2 reading-note prose.
 *
 * Pass the raw markdown content of a reading-note block; returns the same
 * markdown with `(Source: …)` annotations, `Sources: …` footers, and inline
 * `REF-N` markers removed. Markdown structure (headings, lists, emphasis, math)
 * is preserved.
 *
 * @param text - Raw markdown content of a reading-note block.
 * @returns The same markdown with all source-citation markers removed.
 */
export function stripSourceCitations(text: string): string {
  const withoutEditorial = text.replace(EDITORIAL_SOURCES_RE, "");
  const withoutLines = withoutEditorial.replace(SOURCES_LINE_RE, "");
  const withoutInline = withoutLines.replace(INLINE_CITATION_RE, "");
  const tidied = withoutInline.replace(SPACE_BEFORE_PUNCT_RE, "$1");
  return tidied
    .split("\n")
    .map((line) =>
      line.length > 0 && (line[0] === " " || line[0] === "\t")
        ? line
        : line.replace(MULTISPACE_RE, " "),
    )
    .join("\n");
}
