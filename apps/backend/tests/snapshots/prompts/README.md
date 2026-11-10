# Rendered prompt snapshots

One file per condition arm, holding the ChatAdapter message list DSPy sends for a single
section call. `test_rendered_prompt_snapshots.py` fails when a render and its snapshot
disagree, so a prompt change arrives as a diff a reviewer reads rather than as a
difference in results nobody can attribute.

## Regenerating

```
uv run python -m scripts.prompt_snapshots
```

That is the whole procedure. Run it when a change to a signature, a field description, a
projection or a condition profile is intended, and commit the resulting diff with the
change that caused it. Never edit a snapshot by hand — the test compares against a fresh
render, so a hand-edit fails on the next run.

## What is and is not pinned here

Pinned: the instructions, the field list and descriptions, the adapter's field markers,
and the values each condition's policy lets through.

Not pinned: the model's reply. These are inputs.

The lesson is `scripts/prompt_snapshots/fixture.py` — synthetic, and deliberately not the
frozen eval set. Re-freezing the eval set is a separate deliberate act, and a snapshot
that moved with it would report dataset churn as a prompt change. The fixture carries one
of every field some condition gates on, so what a condition drops is visible as an absence
in the diff between two files here.

`P0.md` records no call. Its policy reuses the approved base sections unchanged, so there
is no prompt — an absence stated rather than a file left missing.
