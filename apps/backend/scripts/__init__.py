"""Operational and research scripts (seeds, backfills, audits, snapshot renderers).

Runnable two ways, and both stay working: ``PYTHONPATH=. uv run python scripts/seed_all.py``
for the seed chain ansible drives, and ``uv run python -m scripts.prompt_snapshots`` for the
modules that import each other as ``scripts.<name>``. The package marker is what makes the
second form unambiguous — without it mypy sees ``prompt_snapshots.arms`` and
``scripts.prompt_snapshots.arms`` as two modules for one file, and checks neither.
"""
