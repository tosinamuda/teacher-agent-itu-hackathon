# Generation call stack

This document traces a revision pack from the HTTP request to the DSPy call.
To run an evaluation, see [`experiments/h1_condition_eval/HANDOFF.md`](../experiments/h1_condition_eval/HANDOFF.md).

- Every generation runs as a job, in a process of its own.
- C0–C3 take one code path, and no branch tests a condition label.
- A condition is data: a `ConditionProfile`. Its `generation_policy()` sets the request contents and the validation.
- C4 and P0 make no model call.

Path legend:

| Path starts with | Relative to |
| --- | --- |
| `src/app/`, `experiments/h1_condition_eval/`, `tests/` | `apps/backend/` |
| `application/`, `infrastructure/`, `domain/` | `src/app/domains/artefacts/types/post_class_review_pack/` |
| anything else | `src/app/domains/` |

## 1. Jobs

```text
route handler
  └─ JobQueue(db).add / submit / ensure(kind, *args, subject=...)    app/infra/jobs/queue.py
       └─ one row in the `jobs` table, QUEUED, committed with the caller's transaction
─────────────────────────────── API process ───────────────────────────────
lifespan()                                                            app/lifespan.py
  └─ Runner(JobClaims(...), CONFIG.jobs).run()                        app/infra/jobs/runner.py
       └─ every poll_seconds: JobClaims.claim() → RUNNING, attempts + 1   app/infra/jobs/claims.py
            └─ multiprocessing "spawn" → Process(target=run_job)
─────────────────────────────── job process ───────────────────────────────
run_job(claimed, kind, config, runner_pid)                            app/infra/jobs/process.py
  ├─ _prepare_process()          logging, dspy.configure(lm=build_dspy_lm())
  ├─ _keep_claim thread          renews the lease; exits when the claim or the runner is gone
  ├─ run_in_worker(handler(*args[, redelivered=...]))                app/infra/worker_async.py
  └─ _record(SUCCEEDED | FAILED)
```

Queue:

- `KINDS` in `src/app/infra/jobs/kinds.py` maps each kind to a `module:function` handler.
- `JobQueue.ensure()` returns the unfinished job for the same `(kind, subject)`, or queues one.
- A client follows a job with `GET /jobs/{job_id}`, or `GET /jobs?kind=...&subject=...`.

Runner:

- `JobsConfig` in `src/app/config.py` sets `slots` (4), the poll interval, the lease, the heartbeat and the time limit.
- A process that ends with no recorded outcome goes back to QUEUED, up to the `runs` of its kind.
- A job with a lapsed lease is claimable again.
- `redelivered` goes only to kinds with `told_of_rerun=True`. It is true from the second run.

| Job kind | Queued by | Handler |
| --- | --- | --- |
| `experiments.run_conditioned_execution` | `LaunchExecution` (`POST /experiments/{id}/executions`) | `experiments/application/conditioned_execution.py:conduct_conditioned_execution` |
| `experiments.retry_condition_run` | `retry_condition` (`POST /experiments/{id}/conditions/{code}/retry`) | `experiments/application/condition_retry.py:retry_failed_condition` |
| `content.generate` | `POST /content` | `content/jobs.py:generate_content` |
| `assessments.generate_student_pack` | `LearnerPackGate` via `StudentPackGenerationJobService.enqueue` | `assessments/jobs.py:generate_student_pack` |
| `lesson_plans.generate` | `POST /artefacts/lesson-plans/generate` | `content_engine/jobs.py:generate_lesson_plan` |
| `content_engine.import_lesson_plan` | `POST /plan-imports` | `content_engine/jobs.py:import_lesson_plan` |
| `experiments.author_plan` | `POST /experiments/{id}/plan` | `experiments/jobs.py:draft_experiment_plan` |

The synthetic kinds (`assessments.synthetic_students`, `evaluation.synthetic_*`) also run through this queue.

## 2. Experiment launch

```text
POST /experiments/{experiment_id}/executions         experiments/api/routes.py :: create_experiment_execution
  └─ LaunchExecution(store)(LaunchExecutionInput)    experiments/application/execution_launch.py
       ├─ ensure_plan_is_approved, ensure_no_generation_in_flight,
       │  ensure_h1_conditions_unfrozen (H1)          experiments/application/launch_policy.py
       ├─ create_execution(...)                      the ExperimentExecution row, set to QUEUED
       ├─ store.jobs.add(RUN_CONDITIONED_EXECUTION, execution_id, subject=execution_id)
       └─ store.commit()                             the row and its job in one commit
```

The job process then runs the handler:

```text
conduct_conditioned_execution(execution_id, redelivered=...)   experiments/application/conditioned_execution.py
  ├─ open_execution_context()                        experiments/infrastructure/execution_context.py
  ├─ claim_execution(store, id, redelivered)         experiments/application/execution_lifecycle.py
  ├─ progress_publisher(...)                         live progress for the experiment
  ├─ run_hypothesis(...) → hypothesis_run(...)       match on execution.hypothesis
  │    ├─ H1 → run_h1_execution(..., runner=build_h1_experiment())
  │    └─ H2 → run_h2_execution(..., runner=build_h2_experiment())
  └─ asyncio.shield(_finalize(execution_id, completion))
```

- `claim_execution` skips a terminal row. It skips a RUNNING row unless `redelivered` is true.
- `hypothesis_run` builds only the selected hypothesis. It builds the runner only when `conduct()` runs, because the build opens a language model.
- `_finalize` writes the terminal status through a new session, under `asyncio.shield`. A failed or cancelled attempt still leaves a terminal row.

## 3. H1: C0 to C4

```text
run_h1_execution(...)                                experiments/application/h1_execution.py
  ├─ load_h1_experiment(...) → H1ExperimentInput(run, lesson, design)
  └─ H1Experiment.run(experiment=...)                experiments/review_pack_study/h1/experiment.py
       ├─ for condition in design.conditions_to_generate():      # C0, C1, C2, C3, one at a time
       │    └─ _generate(...) → Result
       │         └─ GenerateBaseReviewPack.generate(
       │                policy=profile_for(H1, condition).generation_policy(), ...)
       ├─ _forked_packs(packs, design.conditions_to_fork())      # C4 gets C3's pack object
       └─ _save_condition_runs(...) → record_condition_runs(...) # one atomic batch
```

- The outer loop is sequential, and the inner loop (below) gathers the units of one condition.
- `conditions_to_generate()` and `conditions_to_fork()` read `generated_by` on each profile. C4 has `generated_by=ConditionCode.C3`.
- Each condition returns a `Result`, so one failure keeps the other packs (`AllConditionsGenerated | SomeConditionsFailed`).
- The harness (`experiments/h1_condition_eval/execution.py`) uses no job. It gathers all (lesson, condition) cells behind `asyncio.Semaphore(6)`.

### The path all four conditions take

```text
GenerateBaseReviewPack.generate(session_plan, policy, sources, specification)
                                                     application/generate_base.py
  ├─ BaseReviewPackRequestBuilder.build(...)         the policy decides what goes in the request
  └─ with capture_prompt_provenance():
       ├─ asyncio.gather(generator.generate_section(request, unit) for unit in request.units)
       └─ FinaliseReviewPack.finalise(policy, request, sections)
```

`generator` is a `SectionGenerator`, a `Protocol` in `application/section_generation.py`.
These classes implement it:

| Class | Where it is used |
| --- | --- |
| `ComposeSection` (`infrastructure/dspy/compose_section.py`) | Production, and the harness arms `compose`, `compose-v2`, `compose-read` |
| `GenerateSection` (`infrastructure/dspy/generate_section.py`) | The harness arm `packed` |
| `GenerateSectionFromSources` | The harness arms `agentic*` |
| `EchoModel` (`tests/condition_leakage_support.py`) | Tests, with no provider |

`infrastructure/generation_wiring.py` builds the production collaborators:

- `generator`: `ComposeSection(contract_mode="leveled", loop=dspy.ReActV2, pipeline=...)`
- `repairer`: `RepairGeneratedSection`
- `critic`: `CritiqueSections`
- `personaliser`: `PersonaliseSection`
- `reviser`: none, so validation never takes the `edit` strategy in production

The harness default is the same arm: `--generator compose-v2 --signatures leveled`.
[`HARNESS-DECISION.md`](../experiments/h1_condition_eval/HARNESS-DECISION.md) records why.

### The model call

```text
ComposeSection.generate_section(request, unit)       infrastructure/dspy/compose_section.py
  └─ aforward(...)
       ├─ contract = composition_contract(signature_for(request.generation_policy))
       ├─ tools = composition_tools(draft, pipeline)                 infrastructure/dspy/tools/section_draft.py
       ├─ agent = dspy.ReActV2(contract, tools=tools, max_iters=16)
       ├─ record_prompt(f"composition.{contract.__name__}", contract)
       └─ run_agent_loop(agent, lm, inputs) → draft.to_section()
```

- The model writes the section through tool calls on a `SectionDraft`. One unit is one agent loop of up to 16 turns.
- `composition_contract` replaces the `section` output with a `done` flag and adds `COMPOSITION_INSTRUCTIONS`.
- The pipeline version selects the tool descriptions. See [`pipeline-versions.md`](pipeline-versions.md).

### Signatures by condition

`signature_for(policy)` in `infrastructure/dspy/contracts/write_section.py` selects the level from
`policy.retrieval.enabled`. It never reads the condition label.

| Condition | Leveled signature (production) | Input fields |
| --- | --- | --- |
| C0 | `WriteObjectiveSection` | `artefact_spec`, `lesson_context`, `unit_context` |
| C1 | `WriteObjectiveSection` | as C0 |
| C2 | `WriteGroundedSection` | as C0, plus `lesson_content` |
| C3 | `WriteGroundedSection` | as C2 |
| C4 | none: C4 forks C3's pack | none |

- `lesson_plan_field_contract(context)` in `infrastructure/dspy/contracts/lesson_context.py` appends a codebook for the plan fields that the condition receives. C0 receives no plan fields and gets no codebook.
- The task text before the codebook is identical for C0 and C1.
- `grounded_lesson_content()` in `infrastructure/dspy/prompt_projection.py` raises when a grounded contract has no evidence. It does not send an empty `lesson_content`.
- The `shared` mode (`WriteSection`, five fields including `policy` and `source_evidence`) is reachable only with `--signatures shared`.

The provenance component on each condition run shows the path that ran:

| `prompt_provenance.components` key | Path |
| --- | --- |
| `composition.ComposeWriteObjectiveSection`, `composition.ComposeWriteGroundedSection` | A compose arm, leveled |
| `composition.ComposeWriteSection` | A compose arm, shared |
| `base_generation.WriteObjectiveSection`, `base_generation.WriteGroundedSection` | `packed`, leveled |
| `base_generation` | `packed`, shared |
| `source_reading` | An `agentic*` arm |

### What each condition changes

| Condition | `ConditionProfile` field that differs | Effect on the call |
| --- | --- | --- |
| C0 | `context=ContextPolicy(generation_unit="objective")` | Units are objectives. The context carries no plan design. |
| C1 | `context=_FULL_LESSON_PLAN_CONTEXT` | Adds entry behaviour, materials, step order, Gagné events, tasks and questions. |
| C2 | `+ retrieval=_SCOPED_RETRIEVAL` | Adds the teacher's note as evidence, and the grounded signature. |
| C3 | `+ validation=_FULL_VALIDATION` | The same generation call, then `FinaliseReviewPack` validates and repairs. |
| C4 | `+ teacher_validation=TeacherValidationPolicy(enabled=True)` | No call. It forks C3's pack. The artefact is written PENDING. |

The profiles are in `experiments/review_pack_study/conditions/profiles.py`.

### C3 validation and repair

For C0–C2, `policy.validation.enabled` is false, and `finalise` returns at once. For C3:

```text
FinaliseReviewPack.finalise(...)                     application/revision/finalise_pack.py
  ├─ _validate(...)
  │    ├─ ReviewPackStructuralValidator.validate(...)   no model
  │    └─ CritiqueSections.review(...)                  MODEL CALL, one per section, gathered
  │         dspy.ChainOfThought(critique_contract(pipeline))   provenance "quality_critique"
  └─ while evaluate_revision(...) says "revise":        at most policy.validation.max_retries (2)
       └─ per section, select_repair_strategy(...) →    application/revision/decisions.py
            preserve    section not implicated, or no unit: no call
            regenerate  findings > max_patchable_findings (3): the generator again,   MODEL CALL
                        with the findings appended to objective_text
            edit        a reviser is wired: EditSection, "section_editing"           MODEL CALL
            repair      otherwise: RepairGeneratedSection, "section_repair"          MODEL CALL
```

- Production wires no reviser. A flagged section gets `regenerate` or `repair`.
- The harness wires `EditSection` with `--repair edit`.

### C4: the teacher's revision

C4 generates nothing in H1. The teacher revises the PENDING pack later:

```text
ArtefactRevisionService.submit_turn(...)             artefact_revision/application/service.py
  └─ ReviewPackRevisionExecutor                      artefact_revision/application/review_pack_executor.py
       └─ ReviseReviewPack                           infrastructure/dspy/revise_review_pack.py
            dspy.ChainOfThought(ApplyReviewPackFeedback)                           MODEL CALL
```

H1 makes four generations and records five condition runs.

## 4. H2: P0 and P1

```text
run_h2_execution(...)                                experiments/application/h2_execution.py
  └─ H2Experiment.run(experiment=...)                experiments/review_pack_study/h2/experiment.py
       ├─ for learner in experiment.learners:        one learner at a time
       │    └─ _learner_packs(...) → Result[LearnerPacks, str]
       │         ├─ P0 = _copy_base_pack(...)        no model call: copies the approved base sections
       │         └─ P1 = await _personalise_pack(...)
       └─ _save_condition_runs(...) → record_condition_runs(...)   one atomic batch
```

- P0 builds its own request under the P0 profile. The rater-visible manifest comes from that request.
- `experiments/review_pack_study/condition_runs/records.py` takes each `condition_profile` from `profile_for(hypothesis, condition_code)`.
- Each learner returns a `Result` (`AllLearnersPersonalised | SomeLearnersFailed`).
- A partial cohort ends the execution FAILED. A failed learner fails at both P0 and P1.

```text
PersonaliseReviewPack.personalise(...)               application/personalise.py
  ├─ build_request(...)                              base_pack_id, learner_states, sources
  ├─ for base_section in base_sections:              sequential, one section at a time
  │    ├─ no learner state for the objective → keep the base section, NO_LEARNER_STATE
  │    └─ else:
  │         scope_unit_evidence(unit, base_section)
  │         PersonaliseSection.personalise_section(...)                            MODEL CALL
  │           provenance f"personalisation.{contract.__name__}"
  │         ├─ wrote a non-visual block → PERSONALISED
  │         └─ only visuals             → keep the base section, EMPTY_RESULT
  └─ FinaliseReviewPack.finalise(policy=P1, ..., base_sections=base_sections)
       checks objective_preservation, source_refs_valid, learner_facing_register;
       max_retries=1                                                              MODEL CALLS
```

- P1 passes `base_sections` to `finalise`. `objective_preservation` compares against them, and repair uses `unit_for_personalisation_repair`.
- The pack holds a `PersonalisationOutcome` per section (`domain/section/personalisation.py`). `experiments/infrastructure/generated_review_pack_record.py` persists it.

## 5. Everyday packs

The teacher's flow uses the same workflow classes with fixed policies from
`domain/generation_policy.py`.

```text
POST /content {type: revision-note, level: class}    content/api/routes.py :: generate_content
  └─ JobQueue.ensure(GENERATE_CONTENT, ...) → 202 {job_id}
       ... job process ...
generate_content(plan_version_id, type, level, pipeline, sources)   content/jobs.py
  └─ ContentService.generate(...) → RevisionPackGenerator            content/infrastructure/generators.py
       └─ build_student_pack_service(pipeline).ensure_base_artefact(...)
            └─ GenerateBaseReviewPack.generate(policy=BASE_REVIEW_PACK_POLICY, ...)   → PENDING class pack
```

```text
LearnerPackGate.request / after_approval             application/learner_pack_gate.py
  └─ StudentPackGenerationJobService.enqueue(...) → JobQueue.add(GENERATE_STUDENT_PACK, generation_id)
       ... job process ...
generate_student_pack(generation_id)                 assessments/jobs.py
  └─ build_student_pack_service(pipeline_that_wrote(class_pack)).generate_for_student(...)
       └─ PersonaliseReviewPack.personalise(policy=PERSONALISED_REVIEW_PACK_POLICY, ...)
```

- The gate queues a learner pack only when the class pack is approved and the learner's evidence is complete.
- A learner pack uses the pipeline version that wrote its class pack.

## 6. Where to look

| Question | File |
| --- | --- |
| What a condition is | `experiments/review_pack_study/conditions/profiles.py` |
| What reached the prompt | `experiments/h1_condition_eval/C0-C1-INPUTS.md` |
| Which signature a run used | `infrastructure/dspy/prompt_fingerprint.py`, and the provenance of the run |
| Product model wiring | `infrastructure/generation_wiring.py` |
| Experiment wiring | `experiments/review_pack_study/wiring.py` |
| Job kinds and handlers | `src/app/infra/jobs/kinds.py` |

The DSPy modules carry no condition logic. Put a condition difference in the
`ConditionProfile → ReviewPackGenerationPolicy` mapping. CI enforces the rule:

| Rule | Check |
| --- | --- |
| Review-pack generation names no condition label | import-linter contract "post-class review-pack does not import experiments" (`pyproject.toml`) |
| C0 and C1 get the same task | `tests/test_level_signatures.py::test_c0_and_c1_are_told_exactly_the_same_thing`, `tests/test_prompt_instructions.py::test_the_two_h1a_arms_are_asked_the_same_task` |
| A condition is told only about its own fields | `tests/test_prompt_instructions.py::test_a_condition_is_told_only_about_the_fields_it_carries` |
| Only permitted fields reach the wire | `tests/test_condition_wire_leakage.py` |
