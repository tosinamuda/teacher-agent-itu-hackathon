"""Compare the lesson note's own generator with the content engine writing the same note.

Run from ``apps/backend``::

    uv run python -m experiments.lesson_note_engine.run --label pre

Add ``--current-from <run>`` to reuse that run's current-generator notes when only the engine
arm's spec changed; each lesson file records the run they came from.

Both arms write every step of each lesson in ``frozen_set.json`` from the plan's fields only,
on the generator model. The engine arm runs the real MCP server and writer in a transaction
that is rolled back, so nothing it stores outlives the run. Both notes render as markdown in
the same conventions: headed parts, numbered examples with marked solutions, and the board.
The run folder holds the blinded review sheet and, apart from it, the key.

``--harness`` runs the engine's writer and checker on another loop (``deepagents`` or
``opencode``) instead of DSPy's, and each lesson records what its note took: writer rounds,
model calls, billed tokens and seconds, or why the draft could not be finished. Before a
batch on a harness, trace one draft with ``trace.py`` and read what reached the endpoint.
"""
