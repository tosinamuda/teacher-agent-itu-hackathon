# Optimized programs (no-linkage / monolithic layer)

Committed DSPy program artifacts for the no-linkage (`curriculum_only`)
single-call drafter. These are **instruction-only** optimized prompts (no
few-shot demos) saved via `dspy.Module.save(...)` as JSON state, and loaded into
`WholeLessonGenerationModule.writer` (a `dspy.ChainOfThought` over
`DraftWholeLessonPlanSignature`) via `writer.load(path)`.

## Files

- `whole_lesson_gepa.json` — RAW GEPA-optimized program (the bake-off winner
  monolithic/cot signature). Promoted from the experiment run
  `experiments/strategy_bakeoff/` (GEPA, `auto=light`, `reasoning=cot`). Kept
  for provenance; **not** the default (see below).
- `whole_lesson_gepa.report.json` — provenance / before-after metrics for the
  run that produced the artifact above.
- `whole_lesson_gepa_nolinkage.json` — **the bundled default** when
  `use_optimized_program=True`. Derived from the raw artifact by
  `scripts/build_nolinkage_optimized_program.py`: it neutralises a grounded
  worksheet demonstration GEPA had frozen into its instructions (which
  hallucinated "distribute a worksheet" on cold-start — confirmed by ablation)
  and appends an explicit no-linkage grounding rule. Re-run that script after
  any new GEPA optimization to refresh it.

## How it is used

Controlled by `app/config.py` → `LessonPlanConfig`:

- `use_optimized_program: bool` — when `True`, the no-linkage module loads the
  artifact below in place of the default signature instructions.
- `optimized_program_path: str | None` — `None` uses the bundled
  `whole_lesson_gepa.json` next to the module; set a path to override.

## Why the default is `False`

GEPA improved **structural compliance** (OPT reward 0.667 → 1.0) but the
small-n **LLM-judge overall score regressed** (4.625 → 4.167) on the held-out
test subtopics. So "optimized" is not an automatic quality win — the choice is
deliberate and is confirmed by manual review + the expert-teacher evaluation
before flipping the default.
