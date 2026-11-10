"""Captioned re-test of the 4 sequencing variants — fair version with real figure captions.

Same variants (regenerate / markers / blocklist / append), but now the manifest feeds each
figure's REAL vision caption, the caption is transcluded as a figcaption, and the writer is
constrained not to invent figure contents. Adds a grounding-fidelity check (prose claims vs.
caption). Two phases so a manual ranking is locked before the LLM judges:

    cd apps/backend
    uv run python -m experiments.sequencing_bakeoff.retest generate
    # ... write .diagnostics/sequencing-bakeoff/manual_judgment.md ...
    uv run python -m experiments.sequencing_bakeoff.retest judge
    uv run python -m experiments.sequencing_bakeoff.render_pdf      # PDF of the content
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import os
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import cast

import dspy

import app.db.metadata  # noqa: F401
from app.db.session import AsyncSessionLocal
from app.shared.json_types import JsonObject
from experiments.sequencing_bakeoff.judge import check_fidelity, judge_step, render_for_judge
from experiments.sequencing_bakeoff.manifest import build_manifest
from experiments.sequencing_bakeoff.metrics import score_variant
from experiments.sequencing_bakeoff.scale import _cell_mean, _mbool, _mint, _mlist
from experiments.sequencing_bakeoff.variants import (
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
]
VARIANT_GENS = [
    ("regenerate", generate_regenerate),
    ("markers", generate_markers),
    ("blocklist", generate_blocklist),
    ("append", generate_append),
]
SEEDS = [0]
# llama-3.3-70b saturated at 5/5 on every cell last run, so it is dropped; gpt-oss is the
# only discriminating reachable judge. The manual ranking is the real cross-check.
QUALITY_MODEL = "openrouter/openai/gpt-oss-120b"
FIDELITY_MODEL = "openrouter/openai/gpt-oss-120b"

_OUT = Path(__file__).resolve().parents[2] / ".diagnostics" / "sequencing-bakeoff"
_RUNS = _OUT / "scale_runs.json"  # render_pdf reads this path
_MANUAL = _OUT / "manual_judgment.md"


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


def _configure() -> None:
    if getattr(dspy.settings, "lm", None) is None:
        dspy.configure(lm=dspy.LM(model=QUALITY_MODEL))
    dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)


async def _load_records() -> dict[str, JsonObject]:
    from sqlalchemy import text

    out: dict[str, JsonObject] = {}
    async with AsyncSessionLocal() as db:
        for topic in TOPICS:
            row = (
                (
                    await db.execute(
                        text(
                            "SELECT record_id, content_text, asset_refs "
                            "FROM textbook_records WHERE record_id=:r"
                        ),
                        {"r": topic.record_id},
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
                out[topic.record_id] = rec
    return out


def phase_generate() -> None:
    _configure()
    records = asyncio.run(_load_records())
    base_lm = dspy.settings.lm
    runs: list[JsonObject] = []
    for topic in TOPICS:
        assets = build_manifest(records[topic.record_id])
        manifest_ids = [asset.ref_id for asset in assets]
        for key, gen in VARIANT_GENS:
            for seed in SEEDS:
                seeded = base_lm.copy(rollout_id=seed, temperature=1.0)
                cell: JsonObject = {"topic": topic.record_id, "variant": key, "seed": seed}
                try:
                    with dspy.context(lm=seeded):
                        variant = gen(assets, objective=topic.objective, grade=topic.grade)
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
                            "rendered": render_for_judge(variant.step),
                            "metrics": dataclasses.asdict(metrics),
                            "judges": {},
                            "error": None,
                        }
                    )
                except Exception as exc:  # noqa: BLE001
                    cell["error"] = f"{type(exc).__name__}: {exc}"[:200]
                runs.append(cell)
                print(
                    f"  gen {topic.record_id}/{key}/seed{seed}: "
                    f"{'ok' if cell.get('error') is None else 'ERR'}",
                    flush=True,
                )
    _OUT.mkdir(parents=True, exist_ok=True)
    _RUNS.write_text(json.dumps(runs, indent=2), encoding="utf-8")
    print(f"\nwrote {len(runs)} cells -> {_RUNS}")
    print(f"NEXT: write {_MANUAL.name}, then run: retest judge")


def phase_judge() -> None:
    _configure()
    runs = json.loads(_RUNS.read_text(encoding="utf-8"))
    qlm, flm = dspy.LM(model=QUALITY_MODEL), dspy.LM(model=FIDELITY_MODEL)

    if _MANUAL.exists():
        print("=" * 88)
        print(f"MANUAL JUDGMENT (locked):\n{_MANUAL.read_text(encoding='utf-8').strip()}")
        print("=" * 88)

    for cell in runs:
        if cell.get("error"):
            continue
        step = cast(JsonObject, cell["step"])
        score = judge_step(step, objective=str(cell["objective"]), grade=str(cell["grade"]), lm=qlm)
        violations = check_fidelity(step, lm=flm)
        cell["judges"] = {
            QUALITY_MODEL: {
                "seq": score.sequencing,
                "coh": score.coherence,
                "ped": score.pedagogy,
                "mean": score.mean,
            }
        }
        cell["fidelity_violations"] = violations
        print(
            f"  {cell['topic']}/{cell['variant']}: quality={score.mean} "
            f"fidelity_violations={len(violations)}",
            flush=True,
        )
    _RUNS.write_text(json.dumps(runs, indent=2), encoding="utf-8")
    print("\n" + _aggregate(runs))


def _fidelity_count(cell: JsonObject) -> int:
    violations = cell.get("fidelity_violations")
    return len(violations) if isinstance(violations, list) else 0


def _aggregate(runs: list[JsonObject]) -> str:
    variants = [key for key, _ in VARIANT_GENS]
    header = (
        f"{len(TOPICS)} topics x {len(variants)} variants x {len(SEEDS)} seed(s), "
        "figure captions fed + transcluded + writer constrained."
    )
    lines = [
        "# Captioned re-test — aggregate\n",
        header + "\n",
        "| variant | valid% | refs clean% | mean llm_chars | quality mean | mean fidelity viol. |",
        "|---|---|---|---|---|---|",
    ]
    for key in variants:
        cells = [c for c in runs if c.get("variant") == key and not c.get("error")]
        if not cells:
            lines.append(f"| {key} | (failed) | | | | |")
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
        quality = [q for c in cells if (q := _cell_mean(c, QUALITY_MODEL)) is not None]
        fid = [_fidelity_count(c) for c in cells]
        q_text = f"{mean(quality):.2f}" if quality else "n/a"
        lines.append(
            f"| {key} | {valid:.0f}% | {clean:.0f}% | {chars:.0f} | {q_text} | {mean(fid):.2f} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["generate", "judge"])
    args = parser.parse_args()
    _ensure_env()
    (phase_generate if args.phase == "generate" else phase_judge)()


if __name__ == "__main__":
    main()
