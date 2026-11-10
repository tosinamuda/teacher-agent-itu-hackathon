# Architecture

How Plan-to-Tutor is built. Terms: [glossary.md](glossary.md); [prototype and study, harness and DSPy](glossary.md#o-words-that-name-more-than-one-thing) say what overlaps. Tables: [data-model.md](data-model.md). Revision-note generation: [revision-note-generation.md](revision-note-generation.md).

## 1. System

- A teacher approves a lesson plan, a lesson note and a class test.
- The system writes a class revision note from them. The teacher approves it.
- Each student takes the class test and gets a personal revision note.
- A researcher runs the same generation under the H1 and H2 conditions.
- Expert raters score the output blind.

Scope: JSS1 mathematics on the Nigerian NERDC curriculum.

## 2. Stack

Turborepo monorepo with two apps and one database.

| Part | Stack | Port |
|---|---|---|
| `apps/frontend` | Vite 8 · React 19 · react-router 7 · TanStack Query · react-hook-form + zod · Tailwind 4 · TipTap · KaTeX | 3000 |
| `apps/backend` | FastAPI · async SQLAlchemy · Alembic · DSPy · litellm · Casbin | 8000 |
| Database | MySQL 9: all data, the background jobs, and live progress | 3306 |

`npm run dev` starts both apps. The API process also runs the background jobs.

## 3. Backend

### Entry point

```text
app/main.py        uvicorn target: prepares the environment, then calls create_app()
app/server.py      create_app(): DSPy setup, CORS, /static mount, error mapping, router
app/router.py      every domain router, plus / and /health
app/lifespan.py    seeds the default school and class, then starts the job runner
app/dspy_setup.py  the generator model, the status logger, the generation log recorder
app/config.py      tunables in code (the environment holds secrets only)
```

### Domain layout

Business logic lives in `src/app/domains/<domain>/`. [`domain-architecture-baseline.md`](../apps/backend/docs/domain-architecture-baseline.md) defines the layers.

| Layer | Holds |
|---|---|
| `api/` | HTTP routes and request/response mapping |
| `application/` | use cases |
| `domain/` | business rules and typed records |
| `infrastructure/` | persistence and external adapters |
| `models/` | SQLAlchemy ORM classes |
| `schemas/` | Pydantic contracts |

### Domain map

| Domain | Owns |
|---|---|
| `users` | Every login identity and its role. Casbin enforces the roles. |
| `school` | Schools, subjects, grade levels, academic years, terms, classes, courses, term-class-subjects |
| `curriculum` | Topics, subtopics, performance objectives, knowledge components, class sessions, themes, class-test items |
| `teaching` | Schemes of work, lesson periods, lesson deliveries, teacher workspaces |
| `learners` | Student profiles |
| `learner_state` | Per-objective learner state, derived from class-test results → [learner-model.md](learner-model.md) |
| `assessments` | Class-test submissions, item responses, the study's classwork, the student-pack job |
| `attachments` | Uploaded photos of original paper work |
| `content` | The `/content` API over lesson plans, lesson notes, class tests and revision notes |
| `artefacts` | Lesson plans, lesson notes, revision notes, content specifications, approvals |
| `artefact_revision` | Revision threads and turns (conversational edits) |
| `expert_content` | Textbook records and the objective-to-textbook linkage → [textbook-curriculum-linkage.md](textbook-curriculum-linkage.md) |
| `experiments` | Studies, experiments, executions, focal cases, condition runs, the imported study record |
| `evaluation` | Raters, assignments, packets, ratings, the source-grounding audit, study ratings |
| `figures` | TikZ drawings, drawn once on the server and served as SVG |
| `jobs` | The `/jobs` API that callers poll |
| `ops` | The ops panel: job and execution health, cancel, redispatch |
| `events` | The activity log |
| `generation_log` | One `generation_events` row per LLM call |
| `tutor` | An in-lesson tutor query endpoint, outside the study |

## 4. The two generation pipelines

The lesson plan is the input specification. The revision note is the evaluated output. Two separate subsystems make them.

| | Lesson-plan drafting | Revision-note generation |
|---|---|---|
| Code | `artefacts/types/lesson_plan/drafting/` | `artefacts/types/post_class_review_pack/` |
| Steps | DSPy modules: objective atomizer, KC extractor, assessment designer, whole-lesson generator | A `ConditionProfile` (`experiments/review_pack_study/conditions/`) sets the context, evidence and validation |
| Output | `PlanVersion.session_plan` | An `artefacts` row of kind `post_class_review_pack` |
| Gate | The teacher approves the plan version (`draft` → `approved`) | The teacher approves the class revision note |

Detail: [revision-note-generation.md](revision-note-generation.md).

## 5. Experiment lifecycle

```text
Investigation (study) ─< Experiment ─< ExperimentExecution (H1 | H2)
                                          ├─< ExperimentFocalCase (one per focal learner)
                                          └─< ExperimentConditionRun (C0–C4, P0–P1)
                                                 └─> ArtefactPlan ─> Artefact
ExperimentExecution ─< EvaluationPacket (blinded) ─> rater ─> EvaluationRating
```

- The API adds a job of kind `experiments.run_conditioned_execution` in the same transaction as the execution.
- H1 generates C0–C3. C4 takes the C3 pack and adds the teacher gate.
- `h1_main_condition_codes()` returns C0–C3. H1 packets and statistics use only these codes.

- H2 personalizes one approved base pack. In the study, the base is the first draw's C3 pack, approved once its validation ran. In the teacher's flow, the base is the C4 pack after the teacher approves it.
- Each condition run keeps `condition_profile`, `validation_result`, `generated_pack`, `model_name` and `prompt_version`.

## 6. LLM calls

- DSPy makes every LLM call. Signatures live with their artefact type, for example `artefacts/types/lesson_plan/drafting/infrastructure/dspy/signatures/`.
- `src/app/infra/llm_models.py` assigns a model to each role:

  | Role | Model | Host |
  |---|---|---|
  | `generator` | `gpt-oss-120b` | Bedrock mantle (OpenAI wire format) |
  | `judge` | `claude-sonnet-4.6` | Bedrock runtime |

- `src/app/infra/dspy_lm.py` builds the one shared LM. The API process and each job process use it.
- The lesson-plan generator loads the GEPA checkpoint `whole_lesson_gepa_nolinkage.json` from `.../dspy/optimized/`.
- `GenerationLogRecorder` writes each call to `generation_events`. `DspyStatusLogger` logs progress. `src/app/config.py` switches each one on.

## 7. Background jobs and progress

### Jobs

Code: `src/app/infra/jobs/`.

- A request adds a row to the `jobs` table and returns `202` with the `job_id`.
- The runner in the API process claims a job with `FOR UPDATE SKIP LOCKED`. It runs each job in a child process, 4 slots by default.

- A running job renews a 120-second lease. A job whose lease lapses runs again, up to the limit of its kind.
- The runner stops a job that runs longer than 2 hours.
- `uq_jobs_active_subject` allows one unfinished job of a kind per subject.
- The frontend polls `/jobs/{job_id}` until the job ends.

### Progress

- Experiment jobs write live progress to `progress_events`, one channel per experiment. Rows expire after one day.
- The websocket `/experiments/{experiment_id}/synthetic/ws` streams that channel to the page.

### Job kinds

| Kind | Work |
|---|---|
| `experiments.run_conditioned_execution` | One H1 or H2 execution |
| `experiments.retry_condition_run` | One failed condition run again |
| `experiments.author_plan` | Draft the plan for an experiment |
| `lesson_plans.generate` | Draft a lesson plan |
| `content.generate` | Generate a lesson note, class test or revision note |
| `assessments.generate_student_pack` | One student's personal revision note |
| `assessments.synthetic_students`, `evaluation.synthetic_rate`, `evaluation.synthetic_teacher`, `evaluation.synthetic_loop` | Synthetic runs |

## 8. Persistence

- MySQL 9 through async SQLAlchemy. Routes get a session from `Depends(get_db)`.
- `src/app/db/metadata.py` imports every ORM model for Alembic.

- Schema migrations: `migrations/schema/versions/` (`uv run alembic upgrade head`).
- Data migrations: `migrations/data/` (`uv run python -m migrations.data.<module>`).

- UUID keys use `CHAR(32)`. Versioned payloads use MySQL `JSON` columns.
- `/static/figures/` serves the textbook images from `src/app/static/figures/`.
- `/figures/<sha256>.svg` serves each TikZ drawing from the `figures` table.

## 9. Frontend

- A single-page app built by Vite. `src/routes/` holds the route tree.
- Each of the 22 features has a folder in `src/features/`. Most have `pages/`, `hooks/` and `components/`.
- Shared code lives in `src/shared/`.

- `shared/components/renderer/ContentBlockRenderer.tsx` renders the blocks `explanation`, `worked_example`, `practice` and `visual`. Lesson plans and revision notes use it.
- Flows by role: [ui-ux.md](ui-ux.md).

## 10. Where to look in code

| Concern | Path |
|---|---|
| App factory, `/static` mount | `src/app/server.py` |
| All routes | `src/app/router.py` |
| Startup and job runner | `src/app/lifespan.py`, `src/app/infra/jobs/` |
| Live progress | `src/app/infra/progress.py` |
| Models per role | `src/app/infra/llm_models.py` |
| ORM registry | `src/app/db/metadata.py` |
| Lesson-plan drafting | `src/app/domains/artefacts/types/lesson_plan/drafting/` |
| Revision-note generation | `src/app/domains/artefacts/types/post_class_review_pack/` |
| Condition profiles and study scale | `src/app/domains/experiments/review_pack_study/conditions/` |
| Experiment models | `src/app/domains/experiments/infrastructure/models.py` |
