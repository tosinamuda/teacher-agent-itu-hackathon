"""Lesson-plan generation strategy bake-off.

Compares generation strategies (baseline / dspy.Refine / dspy.ReAct+verify /
monolithic / RLM) under the pre-registered protocol (the lesson-plan strategy experiment
pre-registration, which is not in this repository).

Integrity backbone (see `check_split`): the deterministic semantic checks are
split into an OPT set (drives self-correction / GEPA) and a HELD-OUT set
(evaluation only, never seen by the optimiser) so we measure generalisation, not
memorisation. The LLM-judge on the real expert rubric is the primary outcome.
"""
