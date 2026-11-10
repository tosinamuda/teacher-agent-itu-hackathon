# DSPy in this codebase

This document lists the DSPy practices the backend applies, with the files that show each one.
For the full call path of a revision pack, see [`generation-call-stack.md`](generation-call-stack.md).

Paths are relative to `apps/backend/`. Two abbreviations:

- `review_pack/` is `src/app/domains/artefacts/types/post_class_review_pack/`.
- `lesson_plan/` is `src/app/domains/artefacts/types/lesson_plan/`.

## Model steps and code steps

A step that code can do as a function over structured data is Python, not a DSPy module.

| Step | Runs as | Where |
| --- | --- | --- |
| Review-pack structural checks | Python | `review_pack/application/validation/structural.py` |
| Repair strategy choice | Python | `review_pack/application/revision/decisions.py` (`select_repair_strategy`) |
| KC checks: source ids, Bloom coverage, KC type, prerequisite cycles | Python | `lesson_plan/drafting/application/precompute/verification.py` |
| Planning on the manual-linkage path | Python | `lesson_plan/drafting/application/precompute/curated_planning.py` |
| Section writing, critique, repair, personalisation | DSPy | `review_pack/infrastructure/dspy/` |
| KC decomposition and lesson drafting | DSPy | `lesson_plan/drafting/infrastructure/dspy/` |

## Signatures

- Each signature is a class-based `dspy.Signature` in `infrastructure/dspy/contracts/` or `infrastructure/dspy/signatures/`.
- The docstring is the instruction text, and each field `desc` is part of the prompt.
- All prompt text is in the signature. A `forward` or `aforward` method adds none.
- Each output field has a type, usually a Pydantic model such as `DraftSection` or `list[ContentFinding]`.

When the instructions depend on data, the code builds the signature with `dspy.make_signature`:

| Builder | What varies | Where |
| --- | --- | --- |
| `signature_for(policy)` | The level and the plan-field codebook of a condition | `review_pack/infrastructure/dspy/contracts/write_section.py` |
| `composition_contract(base)` | A `done` flag in place of the `section` output, plus composition instructions | `review_pack/infrastructure/dspy/compose_section.py` |
| `critique_contract(pipeline)`, `repair_contract(pipeline)` | The text of one pipeline version | `review_pack/infrastructure/dspy/contracts/` |

- `_leveled_signature` is cached on a frozen key, so one condition always gets the same signature object.
- A condition's prompt differs only in the data it receives. The tests in [`generation-call-stack.md`](generation-call-stack.md#6-where-to-look) enforce this.

## Modules

Each model-backed role is one `dspy.Module` in `review_pack/infrastructure/dspy/`:

| Module | Role |
| --- | --- |
| `ComposeSection` | Writes a section through tools (production generator) |
| `GenerateSection` | Writes a section in one call (harness arm `packed`) |
| `CritiqueSections` | Reviews each section against its evidence |
| `RepairGeneratedSection` | Repairs a flagged section |
| `EditSection` | Edits a flagged section (harness only) |
| `PersonaliseSection` | Adapts a base section to one learner |
| `ReviseReviewPack` | Applies the teacher's feedback to a pack |

Each module follows these rules:

- It takes its LM in the constructor and calls under `dspy.settings.context(lm=self.lm)`.
- It prepares the inputs, makes the call and returns a domain object such as `ReviewPackSection`. See `GenerateSection.prepared_call()` and `section_from_draft()`.
- The application layer depends on a `Protocol` (`SectionGenerator`, `SectionCritic`, `SectionRepairer`, `SectionPersonaliser`) in `review_pack/application/section_generation.py`.

`review_pack/infrastructure/generation_wiring.py` is the only product module that names both the
DSPy modules and the operations that use them.

Orchestration is plain Python, not a `dspy.Module`: `GenerateBaseReviewPack`, `FinaliseReviewPack`,
`PersonaliseReviewPack` and `InfrastructurePlanningPipeline`.

Built-in modules in use:

| Module | Use | Where |
| --- | --- | --- |
| `dspy.ChainOfThought` | Most single calls | the modules above, and `lesson_plan/drafting/infrastructure/dspy/modules/` |
| `dspy.ReActV2` | Section composition through native tool calls | `ComposeSection`, wired in `generation_wiring.py` |
| `dspy.Predict` | The lesson-plan final writer when `final_writer_mode="predict"` | `lesson_plan/drafting/infrastructure/dspy/modules/generator.py` |
| `dspy.ReAct` | Harness arms `compose`, `compose-read`, `agentic`, `agentic-file`, `agentic-notebook` | `experiments/h1_condition_eval/generator_arms.py` |
| `dspy.RLM`, `dspy.BestOfN` | Strategy bake-off only | `experiments/strategy_bakeoff/` |

## LM, adapter and callbacks

LM:

- `build_dspy_lm()` in `src/app/infra/dspy_lm.py` builds every LM, with a 300 s request timeout and 8 rate-limit retries.
- `src/app/infra/llm_models.py` assigns a model to each role. The environment holds secrets and an optional `<ROLE>_MODEL` override.

Process setup:

| Process | Setup | Callbacks |
| --- | --- | --- |
| API | `configure_dspy()` in `src/app/dspy_setup.py` | `DspyStatusLogger`, `GenerationLogRecorder`, each behind its `CONFIG` flag |
| Job | `_prepare_process()` in `src/app/infra/jobs/process.py` | `GenerationLogRecorder` when `CONFIG.log_model_calls` is true (default false) |

Adapter:

- The app sets no adapter, so DSPy uses `ChatAdapter`. `review_pack/infrastructure/dspy/prepared_call.py` renders the same format.
- The harnesses call `transport_for(model)` in `src/app/infra/dspy_lm.py`. It returns `JSONAdapter` for a model on `/responses`, else `ChatAdapter`.

## Prompt records

Fingerprints:

- `record_prompt(component, signature)` in `review_pack/infrastructure/dspy/prompt_fingerprint.py` hashes the instructions, field descriptions and schema of a signature.
- `capture_prompt_provenance()` collects the hashes. Each condition run stores them in `prompt_provenance`.

Snapshots:

- `tests/snapshots/prompts/` holds the rendered prompt of each condition arm. `tests/test_rendered_prompt_snapshots.py` compares a fresh render with it.
- After an intended prompt change, run `uv run python -m scripts.prompt_snapshots` and commit the diff with it.
- `tests/snapshots/prompts/evaluated/` holds the prompts that the study sent. Never regenerate them. See [`pipeline-versions.md`](pipeline-versions.md).

## Retry loops

Both products use a bounded loop in Python. A Python check finds the issues, and the next model call receives them.

| Product | Loop | Bound |
| --- | --- | --- |
| Lesson plan | `_refine_attempts()` in `lesson_plan/drafting/application/runtime/service.py` | `CONFIG.lesson_plan.max_refine_attempts` (3) |
| Revision pack | `FinaliseReviewPack.finalise()` in `review_pack/application/revision/finalise_pack.py` | `policy.validation.max_retries` |

## Optimisation

The no-linkage lesson-plan writer can load GEPA-optimized instructions:

1. `experiments/strategy_bakeoff/optimize.py` runs `dspy.GEPA` and saves the raw JSON state.
2. `scripts/build_nolinkage_optimized_program.py` derives the bundled JSON file from it.
3. `WholeLessonGenerationModule` calls `self.writer.load(path)` when `CONFIG.lesson_plan.use_optimized_program` is true.

The files and their history are in
[`optimized/README.md`](../src/app/domains/artefacts/types/lesson_plan/drafting/infrastructure/dspy/optimized/README.md).

## Tests without a model

- `EchoModel` in `tests/condition_leakage_support.py` implements the section-generator protocol with no provider.
- `section_collaborators(lm, pipeline)` in `generation_wiring.py` takes any LM. The snapshot scripts pass a recording LM and capture the real prompt.
- `tests/test_rendered_prompt_matches_the_wire.py` checks that the rendered prompt is the prompt on the wire.
- Validators and decisions are plain Python and have plain unit tests, for example `tests/test_study_pack_decisions.py`.
