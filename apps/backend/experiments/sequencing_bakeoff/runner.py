"""Sequencing bake-off runner — two phases to keep the manual judgment blinded.

    cd apps/backend
    # PHASE 1: generate the 4 variants, compute deterministic metrics, render, SAVE to disk
    uv run python -m experiments.sequencing_bakeoff.runner generate
    # ... read the rendered variants, write your ranking to manual_judgment.md ...
    # PHASE 2: run the LLM judges on the SAVED variants and compare
    uv run python -m experiments.sequencing_bakeoff.runner judge

Saving the generated variants between phases means the judge scores the exact outputs that
were manually judged (no re-generation drift), and the manual ranking is locked first.
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import os
from pathlib import Path

import dspy

import app.db.metadata  # noqa: F401
from app.db.session import AsyncSessionLocal
from app.infra.dspy_lm import active_model_name
from app.shared.json_types import JsonObject
from experiments.sequencing_bakeoff.judge import judge_step
from experiments.sequencing_bakeoff.manifest import build_manifest
from experiments.sequencing_bakeoff.metrics import score_variant
from experiments.sequencing_bakeoff.variants import (
    _GRADE,
    _OBJECTIVE,
    generate_append,
    generate_blocklist,
    generate_markers,
    variant_regenerate,
)

_RECORD_ID = "ch01-b035"
_PLAN_ID = "LP-7616210a25e4429295bead6a58c8853e"
_OUT = Path(__file__).resolve().parents[2] / ".diagnostics" / "sequencing-bakeoff"
_VARIANTS_JSON = _OUT / "variants.json"
_MANUAL_MD = _OUT / "manual_judgment.md"


def _ensure_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            if ("API_KEY" in key or "OPENROUTER" in key) and key.strip() not in os.environ:
                os.environ[key.strip()] = value.strip().strip('"').strip("'")


def _configure_lm() -> str:
    model = os.getenv("DSPY_MODEL") or active_model_name()
    if getattr(dspy.settings, "lm", None) is None:
        dspy.configure(lm=dspy.LM(model=model))
    return model


async def _load() -> tuple[JsonObject, JsonObject]:
    from sqlalchemy import text

    async with AsyncSessionLocal() as db:
        record = (
            (
                await db.execute(
                    text(
                        "SELECT record_id, content_text, asset_refs FROM textbook_records "
                        "WHERE record_id=:r"
                    ),
                    {"r": _RECORD_ID},
                )
            )
            .mappings()
            .first()
        )
        plan = (
            await db.execute(
                text(
                    "SELECT session_plan FROM plan_versions WHERE plan_id=:p "
                    "ORDER BY created_at DESC LIMIT 1"
                ),
                {"p": _PLAN_ID},
            )
        ).scalar()
    if record is None:
        raise RuntimeError(f"record {_RECORD_ID} not found")
    asset_refs = record.get("asset_refs")
    if isinstance(asset_refs, str):
        record["asset_refs"] = json.loads(asset_refs)
    if isinstance(plan, str):
        plan = json.loads(plan)
    steps = plan.get("steps") if isinstance(plan, dict) else None
    stored_step: JsonObject = {"step_id": "v0", "blocks": []}
    for step in steps if isinstance(steps, list) else []:
        if isinstance(step, dict) and any(
            "Powers of ten" in str(b.get("content") or "") for b in step.get("blocks") or []
        ):
            stored_step = step
    return dict(record), stored_step


def phase_generate() -> None:
    from experiments.sequencing_bakeoff.judge import render_for_judge

    model = _configure_lm()
    record, stored_step = asyncio.run(_load())
    assets = build_manifest(record)
    manifest_ids = [asset.ref_id for asset in assets]
    print(f"Model: {model} | manifest: {manifest_ids}\n")

    variants = [
        variant_regenerate(stored_step),
        generate_markers(assets),
        generate_blocklist(assets),
        generate_append(assets),
    ]

    snapshot = []
    for variant in variants:
        metrics = score_variant(
            step=variant.step,
            llm_authored_text=variant.llm_text,
            referenced_ids=variant.referenced_ids,
            manifest_ids=manifest_ids,
        )
        rendered = render_for_judge(variant.step)
        snapshot.append(
            {
                "key": variant.key,
                "label": variant.label,
                "step": variant.step,
                "rendered": rendered,
                "metrics": dataclasses.asdict(metrics),
            }
        )
        print("=" * 88)
        print(f"{variant.label}")
        print("-" * 88)
        print(rendered)
        print(
            f"\n  latex={'VALID' if metrics.latex_valid else 'INVALID: ' + metrics.latex_issue} | "
            f"llm_chars={metrics.llm_authored_chars} total_chars={metrics.final_total_chars} | "
            f"refs valid={metrics.refs_valid} hallucinated={metrics.refs_hallucinated} "
            f"missed={metrics.refs_missed}"
        )

    _OUT.mkdir(parents=True, exist_ok=True)
    _VARIANTS_JSON.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print("\n" + "=" * 88)
    print(f"saved {len(snapshot)} variants -> {_VARIANTS_JSON}")
    print(f"NEXT: write your manual ranking to {_MANUAL_MD}, then run: ... runner judge")


def phase_judge() -> None:
    _configure_lm()
    if not _VARIANTS_JSON.exists():
        raise RuntimeError("run `generate` first")
    snapshot = json.loads(_VARIANTS_JSON.read_text(encoding="utf-8"))

    if _MANUAL_MD.exists():
        print("=" * 88)
        print(f"MANUAL JUDGMENT (locked, {_MANUAL_MD.name}):")
        print(_MANUAL_MD.read_text(encoding="utf-8").strip())
        print("=" * 88 + "\n")

    rows = []
    for entry in snapshot:
        score = judge_step(entry["step"], objective=_OBJECTIVE, grade=_GRADE)
        rows.append((entry["label"], entry["metrics"], score))
        print(
            f"{entry['label']:<16} seq={score.sequencing} coh={score.coherence} "
            f"ped={score.pedagogy} mean={score.mean} | {score.rationale}"
        )

    print("\nLLM-JUDGE RANKING (by mean):")
    for label, metrics, score in sorted(rows, key=lambda r: r[2].mean, reverse=True):
        flags = []
        if not metrics["latex_valid"]:
            flags.append("INVALID-LATEX")
        if metrics["refs_hallucinated"]:
            flags.append("HALLUCINATED-REF")
        print(f"  {score.mean:>4}  {label:<16} {' '.join(flags)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["generate", "judge"])
    args = parser.parse_args()
    _ensure_env()
    (phase_generate if args.phase == "generate" else phase_judge)()


if __name__ == "__main__":
    main()
