r"""Experiment: how to SEQUENCE spliced source assets with LLM prose.

Transclusion keeps the LLM out of the source content, but the asset placement still has to
follow the teaching flow ("look at the table below" must precede the table). Four ways to
let the LLM control order without letting it emit the assets:

  V0  REGENERATE   — current: the LLM writes everything incl. the table (baseline)
  V1  MARKERS      — prose string with {{asset:REF_ID}} markers, split + spliced
  V2  BLOCKLIST    — ordered [prose | ref] block list, refs expanded in place
  V3  APPEND       — prose only, assets dumped after (the naive transclusion)

Metrics (deterministic): LaTeX validity, character economy (LLM-authored vs total), and
reference faithfulness (valid / hallucinated / missed ref ids).

Judging is dual + blinded: a manual ranking is locked to disk FIRST, then an LLM synthetic
rater scores each variant, then the two are compared. Kept OUT of the prod generate path.
"""
