"""CLI wrapper: synthetic LLM-as-judge rating of an experiment's blinded packets.

Thin wrapper over evaluation.application.synthetic_rater.rate_experiment (the same core
the browser-triggered Celery task uses). Raters are clearly labelled "Synthetic Judge —
…" and tagged notes.synthetic=true; not a substitute for the expert-teacher
evaluation in the thesis design.

Usage:  uv run python scripts/synthetic_rate_experiment.py <EXP-id> [persona,persona,...]
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.db.metadata  # noqa: E402,F401  (load ORM models in order — dodges the import cycle)
from app.db.session import AsyncSessionLocal
from app.domains.evaluation.application.synthetic_rater import (  # noqa: E402
    PERSONAS,
    rate_experiment,
)
from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (  # noqa: E402
    SqlAlchemyEvaluationStore,
)
from app.shared.json_types import JsonObject  # noqa: E402


def _personas(result: JsonObject) -> list[str]:
    personas = result.get("personas")
    return [str(persona) for persona in personas] if isinstance(personas, list) else []


async def main(experiment_id: str, personas: list[str]) -> None:
    async with AsyncSessionLocal() as db:
        result = await rate_experiment(
            db,
            identity_store=SqlAlchemyEvaluationStore(db),
            experiment_id=experiment_id,
            personas=personas,
        )
        print(
            f"done — created {result['created']} synthetic ratings across "
            f"{result.get('packets', 0)} packets ({', '.join(_personas(result))})"
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: synthetic_rate_experiment.py <EXP-id> [persona,persona,...]")
        raise SystemExit(1)
    chosen = sys.argv[2].split(",") if len(sys.argv) > 2 else list(PERSONAS)
    asyncio.run(main(sys.argv[1], chosen))
