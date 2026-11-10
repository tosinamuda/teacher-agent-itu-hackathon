"""Experiment: a dspy.ReAct agent that validates and repairs lesson-step content.

Kept OUT of the production generate path (per the "experiment before prod" rule). The
point is to learn — on real defect classes (malformed LaTeX, un-embedded grounded
figures, dangling visual references) — whether a tool-using ReAct loop produces clean,
gate-passing content, and to watch how the validator feedback flows through the
trajectory before deciding what to productionize.

The deterministic validators + repairs here are the reusable contract; the ReAct agent
is one strategy for satisfying it. An INDEPENDENT deterministic gate scores the agent's
output, so the agent never grades its own homework.
"""
