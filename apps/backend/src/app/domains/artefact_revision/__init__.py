"""Artefact revision — human-in-the-loop, chat-style iteration on generated artefacts.

A teacher highlights part of a generated artefact (lesson plan first; study pack
and exit assessment to follow), sends it as context with a free-text instruction,
and the model produces a focused, validated revision — persisted as a new version
in a parent-linked chain. The conversation (thread + turns) is the history; each
turn links to the artefact version it produced, so the iteration is auditable and
replayable.
"""
