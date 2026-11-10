"""P1 prompt-evidence experiment: distilled state card (v1) vs evidence-rich (v2).

Compares the CURRENT production personalisation input (objective state card:
band + bucketed confidence/difficulty + modal misconception code) against the
learner-model spec's full internal LLM input (§ "During personalized content
generation"): per-item answer evidence (question, chosen option, distractor
rationale), canonical 1-5 survey scores, a humanised misconception description,
and session-level interest/affect tone modifiers.

Experiment-before-prod: nothing here touches the production request builder or
signatures. The runner replays a REAL focal case (same base sections, same
learner, same model) under both prompt shapes and writes paired outputs +
captured prompts for independent comparison.
"""
