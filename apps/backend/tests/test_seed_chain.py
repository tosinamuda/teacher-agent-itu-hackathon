"""The seed chain fetches the corpus first, and every step is a script that exists."""

from __future__ import annotations

from pathlib import Path

from scripts.seed_all import BACKEND_DIR, SEED_STEPS


def test_the_corpus_is_fetched_before_any_step_that_reads_it() -> None:
    reading = [step for step in SEED_STEPS if step.startswith("seed_jss1") or "textbook" in step]

    assert SEED_STEPS[0] == "fetch_datasets"
    assert all(SEED_STEPS.index(step) > 0 for step in reading) and reading


def test_every_step_of_the_chain_is_a_script() -> None:
    missing = [
        step for step in SEED_STEPS if not (Path(BACKEND_DIR) / "scripts" / f"{step}.py").is_file()
    ]

    assert missing == []
