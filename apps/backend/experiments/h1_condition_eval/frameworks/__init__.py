"""Section generators driven by an agent framework other than dspy.

Each arm here is `compose-v2` with its driver replaced: the same contract, the same
inputs, the same composition tools writing into the same `SectionDraft`, returned through
the same `assemble_section`. What varies is the loop — langgraph's prebuilt ReAct graph,
Google ADK's agent runner, deepagents' harness — and nothing else, which is the only
condition under which the bake-off is measuring a framework.
"""
