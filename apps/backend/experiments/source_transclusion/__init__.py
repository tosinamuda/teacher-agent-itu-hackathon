r"""Experiment: transclude verbatim source assets instead of regenerating them.

The writer reproduces source content *faithfully* but corrupts the LaTeX *syntax* (drops
`\\` before `\hline`). So the fix isn't to detect+repair the corruption — it's to never let
the LLM re-type content that already exists, valid, in the source. The LLM writes the prose;
deterministic assembly splices the verbatim source table/figure (generalising the figure-embed).

This experiment proves the `\hline` class of bug becomes *structurally impossible* under
transclusion: a verbatim splice is valid by construction and faithful by definition, whereas
the LLM regeneration of the same table is invalid. Kept OUT of the prod generate path.
"""
