"""One-shot database setup: migrate + run the full seed chain.

Replaces running migrations and the six seed scripts by hand. From
``apps/backend``:

    PYTHONPATH=. uv run python scripts/seed_all.py

Steps run in order and the chain stops on the first failure. Pass
``--no-migrate`` to seed only (assumes the schema is already at head).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]

# The single definition of the seed chain — the Ansible deploy runs this script
# (--no-migrate). Order matters: the corpus is fetched first, then the curriculum + textbook
# corpus before the AO linkage that joins them; users (which bind to the seeded
# class/curriculum) come last. The fetch needs HF_TOKEN: the datasets are gated.
SEED_STEPS = (
    "fetch_datasets",
    "seed_casbin_policies",
    "seed_content_specifications",
    "seed_jss1_curriculum",
    "seed_textbook_records",
    "seed_ao_textbook_linkage",
    "seed_curriculum_performance_objectives",
    "seed_minimal_users",
    "seed_msc_study",
    "seed_figures",
)


def _run(label: str, argv: list[str], env: dict[str, str]) -> int:
    print(f"\n=== {label} ===", flush=True)
    result = subprocess.run(argv, cwd=BACKEND_DIR, env=env, check=False)
    if result.returncode != 0:
        print(f"!! step failed: {label} (exit {result.returncode})", file=sys.stderr)
    return result.returncode


def main() -> int:
    migrate = "--no-migrate" not in sys.argv[1:]
    env = {**os.environ, "PYTHONPATH": str(BACKEND_DIR)}

    if migrate:
        rc = _run("alembic upgrade head", [sys.executable, "-m", "alembic", "upgrade", "head"], env)
        if rc != 0:
            return rc

    for step in SEED_STEPS:
        rc = _run(
            f"seed: {step}", [sys.executable, str(BACKEND_DIR / "scripts" / f"{step}.py")], env
        )
        if rc != 0:
            return rc

    print("\n✓ Database setup complete (migrate + seed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
