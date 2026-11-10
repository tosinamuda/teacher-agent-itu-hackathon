"""Compare regenerating a source table vs transcluding it. Run:

    cd apps/backend
    uv run python -m experiments.source_transclusion.runner

Three arms on the real Millions / ch01-b035 step:
  A  REGENERATE   — the stored LLM-written table (what production does today)
  B  TRANSCLUDE   — verbatim source table+figures spliced deterministically (no LLM)
  C  PROSE+SPLICE — the LLM writes ONLY prose, the source assets are spliced after (real LLM call)

Each arm is scored by the deterministic LaTeX validator. The claim under test: regeneration
can be INVALID; transclusion is VALID by construction and faithful by definition.
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import dspy

import app.db.metadata  # noqa: F401  (register ORM models for standalone use)
from app.db.session import AsyncSessionLocal
from app.infra.dspy_lm import active_model_name
from app.shared.json_types import JsonObject
from experiments.content_repair.validators import block_list, validate_latex, validate_step
from experiments.source_transclusion.transclude import assemble_step, source_blocks

_RECORD_ID = "ch01-b035"
_PLAN_ID = "LP-7616210a25e4429295bead6a58c8853e"


class WriteStepProse(dspy.Signature):
    """Write ONLY the teacher-facing explanation prose for a lesson step.

    The source table and figures are spliced in automatically AFTER your text — DO NOT
    reproduce any table, array (\\begin{array}...), equation, or image yourself. Refer to
    them in words (e.g. "the table below"). Explain the concept clearly for the objective
    and grade."""

    objective: str = dspy.InputField()
    grade: str = dspy.InputField()
    available_assets: str = dspy.InputField(desc="What will be spliced in after your prose.")
    explanation_markdown: str = dspy.OutputField(
        desc="Teacher explanation prose only. No tables, arrays, or images."
    )


def _ensure_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if ("API_KEY" in key or "OPENROUTER" in key) and key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def _configure_lm() -> str:
    model = os.getenv("DSPY_MODEL") or active_model_name()
    if getattr(dspy.settings, "lm", None) is None:
        dspy.configure(lm=dspy.LM(model=model))
    return model


def _verdict(step: JsonObject) -> str:
    issues = validate_step(step, []).issues
    latex_issues = [i for i in issues if "hline" in i or "begin/\\end" in i or "$$" in i]
    return "VALID" if not latex_issues else f"INVALID ({len(latex_issues)}): {latex_issues[0][:70]}"


async def _load() -> tuple[JsonObject, str]:
    from sqlalchemy import text

    async with AsyncSessionLocal() as db:
        record = (
            (
                await db.execute(
                    text(
                        "SELECT record_id, content_text, asset_refs FROM textbook_records "
                        "WHERE record_id=:rid"
                    ),
                    {"rid": _RECORD_ID},
                )
            )
            .mappings()
            .first()
        )
        plan = (
            await db.execute(
                text(
                    "SELECT session_plan FROM plan_versions WHERE plan_id=:pid "
                    "ORDER BY created_at DESC LIMIT 1"
                ),
                {"pid": _PLAN_ID},
            )
        ).scalar()

    if record is None:
        raise RuntimeError(f"source record {_RECORD_ID} not found")
    asset_refs = record.get("asset_refs")
    if isinstance(asset_refs, str):
        record["asset_refs"] = json.loads(asset_refs)
    if isinstance(plan, str):
        plan = json.loads(plan)
    steps = (plan or {}).get("steps") if isinstance(plan, dict) else []
    stored_table = ""
    for step in steps or []:
        for block in (step.get("blocks") if isinstance(step, dict) else None) or []:
            if isinstance(block, dict) and "Powers of ten" in str(block.get("content") or ""):
                stored_table = str(block["content"])
    return dict(record), stored_table


def main() -> None:
    _ensure_env()
    model = _configure_lm()
    record, stored_table = asyncio.run(_load())
    print(f"Model: {model}\nSource record: {record['record_id']}\n")

    # ---- Arm A: REGENERATE (what production does today) ----
    print("=" * 84)
    print("ARM A — REGENERATE (LLM re-typed the table; this is the stored output)")
    arm_a: JsonObject = {
        "step_id": "stepA",
        "blocks": [{"id": "a", "type": "explanation", "content": stored_table}],
    }
    print("  verdict:", _verdict(arm_a))

    # ---- Arm B: TRANSCLUDE (verbatim source, deterministic) ----
    print("=" * 84)
    print("ARM B — TRANSCLUDE (verbatim source table + figures, no LLM)")
    blocks_b = source_blocks(record, step_id="stepB")
    arm_b: JsonObject = {"step_id": "stepB", "blocks": blocks_b}
    math_blocks = [b for b in blocks_b if b["type"] == "explanation"]
    fig_blocks = [b for b in blocks_b if b["type"] == "visual"]
    print(
        f"  spliced {len(math_blocks)} verbatim math block(s) + {len(fig_blocks)} figure(s), "
        f"all tagged source_record_id={record['record_id']!r}"
    )
    print("  verdict:", _verdict(arm_b))
    # faithfulness is definitional, but show the validator agrees the source itself is valid
    for mb in math_blocks:
        print("  source math block validate_latex:", validate_latex(str(mb["content"])) or "VALID")

    # ---- Arm C: PROSE + SPLICE (real LLM writes prose only) ----
    print("=" * 84)
    print("ARM C — PROSE+SPLICE (LLM writes prose; source assets spliced after)")
    writer = dspy.Predict(WriteStepProse)
    prediction = writer(
        objective=(
            "Explain the concept of a million using the powers-of-ten table and counting charts."
        ),
        grade="JSS1",
        available_assets=(
            "A powers-of-ten table (Ten ... Billion) and two counting charts from the textbook."
        ),
    )
    prose = str(prediction.explanation_markdown)
    reproduced = "\\begin{array}" in prose
    arm_c = assemble_step(
        step_id="stepC",
        title="Understanding millions",
        prose_markdown=prose,
        grounded_records=[record],
    )
    blocks_c = block_list(arm_c)
    print(f"  LLM prose length: {len(prose)} chars | reproduced a table itself? {reproduced}")
    print(f"  prose preview: {prose[:140]!r}")
    print(
        f"  assembled step: {len(blocks_c)} blocks "
        f"({sum(b.get('type') == 'visual' for b in blocks_c)} visual)"
    )
    print("  verdict:", _verdict(arm_c))

    print("\n" + "=" * 84)
    print("SUMMARY:")
    print("  A regenerate :", _verdict(arm_a))
    print("  B transclude :", _verdict(arm_b))
    print("  C prose+splice:", _verdict(arm_c))


if __name__ == "__main__":
    main()
