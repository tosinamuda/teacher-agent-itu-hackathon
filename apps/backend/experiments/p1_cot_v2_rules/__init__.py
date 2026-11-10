"""Deconfounding arm: ChainOfThought with the ReAct-v2 rules, no tool.

PROMOTED 2026-06-11: this arm matched most of ReAct-v2's gains at 1x cost
(soft attributions 12 -> 6 vs ReAct's 4; targeting equal), so the rules were
appended to the production SectionPersonalisation. Kept for the
run-history trail.

ReAct-v2 beat production on attribution noise (soft 4 vs 12) and targeting —
but its signature carried EXTRA instructions production lacked, so the
comparison confounds module (ReAct + read_source) with instructions
(targeting-first ordering, never-substitute, arithmetic check, verify-before-
citing). This arm gives ChainOfThought the same rules, with the tool protocol
rephrased as "re-read the excerpt in source_evidence" — if it matches ReAct-v2,
the win is the instructions at 1x cost; if not, the tool loop earns its 4x.

    uv run python -m experiments.p1_prompt_eval.runner \
      --variant experiments.p1_cot_v2_rules.signature:PersonaliseWithV2Rules
"""
