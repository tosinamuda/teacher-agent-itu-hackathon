"""Candidate personaliser: dspy.ReAct with a read_source verification tool.

Hypothesis: the residual hallucination (false provenance — attributing
generated practice problems to the textbook, loose method attributions) comes
from the model citing sources it never actually inspected. ReAct gives it a
``read_source`` tool and an explicit rule: read an excerpt before citing it,
never attribute anything the tool did not return.

Run against the production prompt via the eval harness:

    uv run python -m experiments.p1_prompt_eval.runner \
      --variant experiments.p1_react_personaliser.variant:build_react_personaliser

then compare + judge with reward.py. Experiment-before-prod: nothing imports
this from production code.
"""
