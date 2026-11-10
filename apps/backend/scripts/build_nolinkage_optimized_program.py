"""Derive a no-linkage-safe variant of the GEPA-optimized monolithic program.

GEPA was optimized on GROUNDED subtopics, so its instructions froze a
grounded-context demonstration —

    teacher_activities: ["Distribute worksheet containing exercises
                          ch05-b015-i02 & ch05-b015-i03", ...]

— that references real textbook record IDs. Carried into the production
monolithic path (which only ever serves NO-LINKAGE / cold-start subtopics with
no records), the model imitates that sentence and hallucinates "distribute a
worksheet" with nothing behind it. A controlled ablation confirmed this single
sentence is the cause: removing it yields a clean plan.

This script derives `whole_lesson_gepa_nolinkage.json` from the raw
`whole_lesson_gepa.json` by:
  1. neutralising the grounded worksheet demonstration,
  2. appending an explicit no-linkage grounding rule, and
  3. migrating the step shape it describes to the current `PlanStep` schema.

Step (3) is a stopgap, not a substitute for re-optimizing. The GEPA run predates
`activities: [{who, what}]` replacing the parallel teacher/student lists, so its
instructions still show the superseded shape and the generator would emit output the
schema rejects. Rewriting the shape here keeps the raw artifact untouched as a
provenance record, but the SCORE that selected these instructions was measured against
the old output format and no longer certifies them. Re-run GEPA before trusting the
drafting path.

Re-run after any new GEPA optimization to refresh the no-linkage artifact:
    uv run python scripts/build_nolinkage_optimized_program.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

OPTIMIZED_DIR = Path(
    "src/app/domains/artefacts/types/lesson_plan/drafting/infrastructure/dspy/optimized"
)
RAW = OPTIMIZED_DIR / "whole_lesson_gepa.json"
OUT = OPTIMIZED_DIR / "whole_lesson_gepa_nolinkage.json"

# The exact grounded demonstration that misfires on no-linkage (verified by ablation).
WORKSHEET_DEMO = "Distribute worksheet containing exercises ch05-b015-i02 & ch05-b015-i03"
NEUTRAL = "Facilitate the assessment and monitor student responses"

# The step shape the GEPA run froze, and its replacement. `mode` is dropped: it is not
# represented in the data collected from the expert.
OLD_SHAPE = (
    '  "estimated_minutes": <int>,\n'
    '  "mode": "<Demonstration|Discussion|Individual|Group>",\n'
    '  "teacher_activities": ["list", "of", "actions"],\n'
    '  "student_activities": ["list", "of", "actions"]'
)
NEW_SHAPE = (
    '  "estimated_minutes": <int>,\n'
    '  "activities": [{"who": "teacher|student", "what": "<action>"}]'
)
# Worked examples inside the instructions carry the same shape; a template naming
# `activities` beside an example naming `teacher_activities` shows the model two
# formats at once.
EXAMPLE_BLOCK = re.compile(
    r'(\s*)"mode"\s*:\s*"[^"]*",\n'
    r'\s*"teacher_activities"\s*:\s*\[(.*?)\],\n'
    r'\s*"student_activities"\s*:\s*\[(.*?)\](?=[,\n])',
    re.S,
)


def _migrate_step_shape(instructions: str) -> str:
    def convert(match: re.Match[str]) -> str:
        indent = match.group(1)
        items = [
            f'{{"who":"{who}","what":"{value}"}}'
            for raw, who in ((match.group(2), "teacher"), (match.group(3), "student"))
            for value in re.findall(r'"((?:[^"\\]|\\.)*)"', raw)
        ]
        inner = ",\n".join(f"{indent}  {item}" for item in items)
        return f'{indent}"activities":[\n{inner}\n{indent}]'

    return EXAMPLE_BLOCK.sub(convert, instructions.replace(OLD_SHAPE, NEW_SHAPE))


NO_LINKAGE_RULE = (
    "\n\n### NO-LINKAGE GROUNDING (curriculum-only / cold-start lessons)\n"
    "This lesson has NO textbook records to ground on. Therefore:\n"
    "- Do NOT mention, distribute, or refer to worksheets, answer keys, response "
    "cards, or 'attached' materials in ANY step. A review study pack is "
    "self-contained — such artefacts do not exist.\n"
    "- The practice and assessment blocks you generate ARE the assessment. Refer "
    "to them as 'the questions/tasks below', never as an external worksheet or "
    "handout.\n"
    "- Use ONLY the instructional_materials listed in the curriculum input. Do not "
    "invent additional materials, page numbers, or textbook record IDs."
)


def main() -> int:
    data = json.loads(RAW.read_text(encoding="utf-8"))
    instructions = data["predict"]["signature"]["instructions"]

    demo_count = instructions.count(WORKSHEET_DEMO)
    if demo_count != 1:
        raise SystemExit(
            f"expected exactly 1 worksheet demonstration, found {demo_count}; "
            "the raw artifact changed — update WORKSHEET_DEMO."
        )

    cleaned = _migrate_step_shape(instructions.replace(WORKSHEET_DEMO, NEUTRAL) + NO_LINKAGE_RULE)
    data["predict"]["signature"]["instructions"] = cleaned
    # Mark provenance so the artifact is self-describing.
    data.setdefault("metadata", {})["derived_from"] = "whole_lesson_gepa.json"
    data["metadata"]["derivation"] = (
        "neutralise grounded worksheet demo + no-linkage rule + migrate step shape"
    )
    data["metadata"]["shape_migrated"] = "activities[{who,what}]; mode dropped"
    data["metadata"]["gepa_score_stale"] = (
        "instructions were optimized against the pre-activities step shape"
    )

    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"  worksheet demo neutralised: {demo_count} occurrence")
    print(f"  instructions length: {len(instructions)} -> {len(cleaned)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
