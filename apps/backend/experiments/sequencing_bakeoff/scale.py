"""Scaled sequencing bake-off: T topics x V variants x N seeds x 2 judge models.

    cd apps/backend
    uv run python -m experiments.sequencing_bakeoff.scale

Generates every (topic, variant, seed) cell with the DSPy cache OFF (so seeds are
independent draws), scores each deterministically, judges each with two different models,
then aggregates (grand mean +/- std, validity rate, ref faithfulness, char economy, and
paired V2-vs-others win-rates) and writes FINDINGS.md. Raw runs -> .diagnostics (gitignored).
"""

from __future__ import annotations

import asyncio
import dataclasses
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from typing import cast

import dspy

import app.db.metadata  # noqa: F401
from app.db.session import AsyncSessionLocal
from app.infra.dspy_lm import active_model_name
from app.shared.json_types import JsonObject
from experiments.sequencing_bakeoff.judge import judge_step
from experiments.sequencing_bakeoff.manifest import Asset, build_manifest
from experiments.sequencing_bakeoff.metrics import score_variant
from experiments.sequencing_bakeoff.variants import (
    Variant,
    generate_append,
    generate_blocklist,
    generate_markers,
    generate_regenerate,
)


@dataclass
class Topic:
    record_id: str
    objective: str
    grade: str = "JSS1"


TOPICS = [
    Topic(
        "ch01-b035",
        "Explain the concept of a million using the powers-of-ten table and counting charts.",
    ),
    Topic(
        "ch01-b017",
        "Explain decimal place values (tenths, hundredths) using the place-value table.",
    ),
    Topic(
        "ch04-b018",
        "Explain how improper fractions have equivalent fractions using the worked diagrams.",
    ),
]
VARIANT_GENS = [
    ("regenerate", generate_regenerate),
    ("markers", generate_markers),
    ("blocklist", generate_blocklist),
    ("append", generate_append),
]
SEEDS = [0, 1, 2]
JUDGE_MODELS = [
    "openrouter/openai/gpt-oss-120b",
    "openrouter/meta-llama/llama-3.3-70b-instruct",
]
FOCAL = "blocklist"  # the variant whose win we are stress-testing

_OUT = Path(__file__).resolve().parents[2] / ".diagnostics" / "sequencing-bakeoff"
_RAW = _OUT / "scale_runs.json"
_FINDINGS = Path(__file__).resolve().parent / "FINDINGS.md"


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


async def _load_records(record_ids: list[str]) -> dict[str, JsonObject]:
    from sqlalchemy import text

    out: dict[str, JsonObject] = {}
    async with AsyncSessionLocal() as db:
        for rid in record_ids:
            row = (
                (
                    await db.execute(
                        text(
                            "SELECT record_id, content_text, asset_refs "
                            "FROM textbook_records WHERE record_id=:r"
                        ),
                        {"r": rid},
                    )
                )
                .mappings()
                .first()
            )
            if row is not None:
                rec = dict(row)
                asset_refs = rec.get("asset_refs")
                if isinstance(asset_refs, str):
                    rec["asset_refs"] = json.loads(asset_refs)
                out[rid] = rec
    return out


def _gen(key: str, assets: list[Asset], topic: Topic) -> Variant:
    fn = dict(VARIANT_GENS)[key]
    return fn(assets, objective=topic.objective, grade=topic.grade)


def _generate_runs(records: dict[str, JsonObject]) -> list[JsonObject]:
    base_lm = dspy.settings.lm
    runs: list[JsonObject] = []
    for topic in TOPICS:
        assets = build_manifest(records[topic.record_id])
        manifest_ids = [asset.ref_id for asset in assets]
        for key, _gen_fn in VARIANT_GENS:
            for seed in SEEDS:
                seeded = base_lm.copy(rollout_id=seed, temperature=1.0)
                cell: JsonObject = {"topic": topic.record_id, "variant": key, "seed": seed}
                try:
                    with dspy.context(lm=seeded):
                        variant = _gen(key, assets, topic)
                    metrics = score_variant(
                        step=variant.step,
                        llm_authored_text=variant.llm_text,
                        referenced_ids=variant.referenced_ids,
                        manifest_ids=manifest_ids,
                    )
                    cell.update(
                        {
                            "objective": topic.objective,
                            "grade": topic.grade,
                            "step": variant.step,
                            "metrics": dataclasses.asdict(metrics),
                            "error": None,
                        }
                    )
                except Exception as exc:  # noqa: BLE001 - record + continue
                    cell["error"] = f"{type(exc).__name__}: {exc}"[:200]
                runs.append(cell)
                done = "ok" if cell.get("error") is None else "ERR"
                print(f"  gen {topic.record_id}/{key}/seed{seed}: {done}", flush=True)
    return runs


def _judge_runs(runs: list[JsonObject]) -> None:
    judge_lms = {name: dspy.LM(model=name) for name in JUDGE_MODELS}
    for cell in runs:
        cell["judges"] = {}
        if cell.get("error") is not None:
            continue
        for name, lm in judge_lms.items():
            try:
                score = judge_step(
                    cast(JsonObject, cell["step"]),
                    objective=str(cell["objective"]),
                    grade=str(cell["grade"]),
                    lm=lm,
                )
                cell["judges"][name] = {
                    "seq": score.sequencing,
                    "coh": score.coherence,
                    "ped": score.pedagogy,
                    "mean": score.mean,
                }
            except Exception as exc:  # noqa: BLE001
                cell["judges"][name] = {"error": f"{type(exc).__name__}: {exc}"[:120]}
        print(f"  judge {cell['topic']}/{cell['variant']}/seed{cell['seed']}: done", flush=True)


def _cell_mean(cell: JsonObject, judge: str) -> float | None:
    judges = cast(JsonObject, cell.get("judges") or {})
    score = cast(JsonObject, judges.get(judge) or {})
    value = score.get("mean")
    return float(value) if isinstance(value, (int, float)) else None


def _met(cell: JsonObject) -> JsonObject:
    return cast(JsonObject, cell.get("metrics") or {})


def _mbool(cell: JsonObject, key: str) -> bool:
    return bool(_met(cell).get(key))


def _mint(cell: JsonObject, key: str) -> int:
    value = _met(cell).get(key)
    return int(value) if isinstance(value, (int, float)) else 0


def _mlist(cell: JsonObject, key: str) -> list[object]:
    value = _met(cell).get(key)
    return value if isinstance(value, list) else []


def _aggregate(runs: list[JsonObject], stamp: str) -> str:
    variants = [key for key, _ in VARIANT_GENS]
    lines: list[str] = [f"## Run {stamp}", ""]
    lines.append(
        f"Design: {len(TOPICS)} topics x {len(variants)} variants x {len(SEEDS)} seeds "
        f"({len(TOPICS) * len(variants) * len(SEEDS)} cells), "
        f"judged by {len(JUDGE_MODELS)} models.\n"
    )
    failures = [c for c in runs if c.get("error")]
    if failures:
        lines.append(f"Generation failures: {len(failures)} — {[c['variant'] for c in failures]}\n")

    # Per-variant deterministic + judge aggregates
    lines.append("## Per-variant aggregates\n")
    lines.append(
        "| variant | valid% | refs clean% | mean llm_chars | "
        + " | ".join(f"{m.split('/')[-1]} mean±sd" for m in JUDGE_MODELS)
        + " |"
    )
    lines.append("|---|---|---|---|" + "---|" * len(JUDGE_MODELS))
    for key in variants:
        cells = [c for c in runs if c["variant"] == key and not c.get("error")]
        if not cells:
            lines.append(f"| {key} | (all failed) | | | |")
            continue
        valid = mean(1.0 if _mbool(c, "latex_valid") else 0.0 for c in cells) * 100
        clean = (
            mean(
                0.0 if _mlist(c, "refs_hallucinated") or _mlist(c, "refs_missed") else 1.0
                for c in cells
            )
            * 100
        )
        chars = mean(_mint(c, "llm_authored_chars") for c in cells)
        judge_cols = []
        for jm in JUDGE_MODELS:
            vals = [v for c in cells if (v := _cell_mean(c, jm)) is not None]
            judge_cols.append(f"{mean(vals):.2f}±{pstdev(vals):.2f}" if vals else "n/a")
        lines.append(
            f"| {key} | {valid:.0f}% | {clean:.0f}% | {chars:.0f} | "
            + " | ".join(judge_cols)
            + " |"
        )

    # Paired win-rate: FOCAL vs each other variant, per judge, across matched (topic,seed) cells
    lines.append("\n## Paired win-rate (FOCAL = " + FOCAL + ", per judge, across matched cells)\n")
    for jm in JUDGE_MODELS:
        lines.append(f"\n**Judge {jm.split('/')[-1]}**\n")
        lines.append("| vs | wins | ties | losses | win-rate |")
        lines.append("|---|---|---|---|---|")
        for other in variants:
            if other == FOCAL:
                continue
            wins = ties = losses = 0
            for topic in TOPICS:
                for seed in SEEDS:
                    fcell = next(
                        (
                            c
                            for c in runs
                            if c["variant"] == FOCAL
                            and c["topic"] == topic.record_id
                            and c["seed"] == seed
                        ),
                        None,
                    )
                    ocell = next(
                        (
                            c
                            for c in runs
                            if c["variant"] == other
                            and c["topic"] == topic.record_id
                            and c["seed"] == seed
                        ),
                        None,
                    )
                    if not fcell or not ocell:
                        continue
                    fv, ov = _cell_mean(fcell, jm), _cell_mean(ocell, jm)
                    if fv is None or ov is None:
                        continue
                    if fv > ov:
                        wins += 1
                    elif fv < ov:
                        losses += 1
                    else:
                        ties += 1
            total = wins + ties + losses
            rate = f"{(wins + 0.5 * ties) / total:.0%}" if total else "n/a"
            lines.append(f"| {FOCAL} vs {other} | {wins} | {ties} | {losses} | {rate} |")

    return "\n".join(lines) + "\n"


def main() -> None:
    _ensure_env()
    model = os.getenv("DSPY_MODEL") or active_model_name()
    if getattr(dspy.settings, "lm", None) is None:
        dspy.configure(lm=dspy.LM(model=model))
    dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)

    records = asyncio.run(_load_records([t.record_id for t in TOPICS]))
    print(f"Model: {model} | topics: {list(records)} | seeds: {SEEDS} | judges: {JUDGE_MODELS}\n")

    print("GENERATION:")
    runs = _generate_runs(records)
    print("\nJUDGING:")
    _judge_runs(runs)

    _OUT.mkdir(parents=True, exist_ok=True)
    _RAW.write_text(json.dumps(runs, indent=2), encoding="utf-8")
    # Append-only historical log: never overwrite prior runs — each run is a dated section.
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    report = _aggregate(runs, stamp)
    log_header = "# Sequencing bake-off — findings log (append-only)\n"
    existing = _FINDINGS.read_text(encoding="utf-8") if _FINDINGS.exists() else log_header
    _FINDINGS.write_text(existing.rstrip() + "\n\n---\n\n" + report, encoding="utf-8")
    print("\n" + report)
    print(f"raw -> {_RAW}\nfindings -> {_FINDINGS}")


if __name__ == "__main__":
    main()
