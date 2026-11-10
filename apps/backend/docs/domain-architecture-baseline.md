# Backend domain architecture baseline

The directory layout, layer meanings, domain map and data keys for `apps/backend/app`.

- The callable boundary and module size: [`application-boundaries.md`](application-boundaries.md)
- Transactions and data access: [`persistence-boundaries.md`](persistence-boundaries.md)
- Why a seam, layer or constant earns its place: [`code-design-rules.md`](code-design-rules.md)

## Vocabulary

| Question | Where to look |
| --- | --- |
| What does a research or product term mean? H1/H2, C0–C4, P0–P1, focal learner, evaluation packet, plan version | [`docs/glossary.md`](../../../docs/glossary.md) |
| What does a code-shape term mean? layer names, application record, port, store, reader | [`code-vocabulary.md`](code-vocabulary.md) |

`Policy` has two senses, and both glossaries define it. In the thesis, a policy is a frozen
config that defines a condition, such as `ContextPolicy`. In the code, `policy.py` holds a
pure precondition with no I/O.

## Top-level layout

```text
app/
  main.py          # `uvicorn app.main:app`: prepares the environment, then builds the app
  environment.py   # prepare_environment(): reads .env before any module loads
  server.py        # create_app(): routes, CORS, static files, error mapping
  router.py        # every domain router, in match order
  lifespan.py      # what the API does as it starts and stops
  dspy_setup.py    # configure_dspy(): the API process's model client and callbacks
  config.py        # CONFIG: non-secret tunables, in code
  db/              # engine, session, Base, model metadata, status_enum()
  infra/           # the job queue and runner (jobs/), LLM clients, job progress
  shared/          # contracts that two or more domains share
  domains/         # one package per business domain
migrations/
  schema/          # Alembic schema migrations
  data/            # data migrations and their records
```

Background work runs as rows in the MySQL `jobs` table. `src/app/infra/jobs/kinds.py` names every
job kind and its handler. The API process's runner claims each job and runs it in its own process.

## Layers

| Layer | Holds | Never holds |
| --- | --- | --- |
| `api/` | FastAPI routes, request parsing, response mapping, status codes, HTTP dependency wiring | workflow orchestration, persistence reads and writes, DSPy calls |
| `application/` | use cases with one input and one output, calls to ports and to other domains' use cases, transaction timing | FastAPI concerns, ORM class definitions, duplicate schemas, transport errors |
| `domain/` | business rules, transitions, normalization, typed domain values | HTTP, database and framework knowledge |
| `infrastructure/` | SQLAlchemy repositories and stores, ORM models, DSPy modules and signatures, file caches, library adapters | the use-case sequence |
| `validation/` | validation operations and typed results, when more than one flow uses them | Pydantic request and response contracts |

- Each layer means the same thing in every domain. A domain creates only the layers it needs.
- A subdomain has its own layers at any depth. `scripts/layer_paths.py` defines the four layer
  names for every structural guard, and `tests/test_layer_paths.py` fails a guard that walks a
  layer by its own glob.

## File and package names

| Name | Holds only |
| --- | --- |
| `models/`, `infrastructure/models.py` | SQLAlchemy ORM classes |
| `schemas/`, `schemas.py` | Pydantic contracts |
| `types.py` | internal typed records: dataclasses, `TypedDict`, `Protocol`, aliases |
| `deps.py`, `api/deps.py` | dependency wiring: a composition root |
| `infrastructure/wiring.py` | the composition root for jobs and other callers |
| `jobs.py` | job handlers that `src/app/infra/jobs/kinds.py` names |
| `application/errors.py` | the domain's application errors |

- Put no SQLAlchemy model in `schemas`.
- Put no Pydantic contract in `types.py`.
- Define each schema class once. Import it everywhere else.

## Dependency contracts

`make imports` runs import-linter against the contracts in `pyproject.toml`.
`make pylint` fails on import cycles.

| Contract | Forbids |
| --- | --- |
| `application does not import infrastructure directly` | a listed `application/` package importing a listed `infrastructure/` package; each exemption names its exit story |
| `application does not import api transport` | a listed `application/` package importing a listed `api/` package; each exemption names its exit story |
| `api transport does not directly import peer-domain code` | a listed `api/` package importing `curriculum.domain` |
| `leaf/reference domains import no peer domain` | `curriculum`, `events`, `expert_content`, `learner_state` and `generation_log` importing another domain |
| `artefacts core domain imports no peer domain and no content type` | `artefacts.core.domain` importing another domain or a content type |
| `post-class review-pack does not import experiments` | the review-pack product knowing that the study exists |
| `generation reads condition profiles, never condition labels` | review-pack DSPy code importing `experiments.domain` |
| `evaluation transport+persistence do not DIRECTLY import experiments (PR-1 win)` | `evaluation.api` and `evaluation.infrastructure` importing `experiments`, apart from `evaluation/api/deps.py` |

- `pyproject.toml` lists the packages each contract covers. Add a new domain's packages there.
- `tests/test_import_contract_ceilings.py` holds each exemption list to an exact size.
- A `domain/` layer imports no peer domain. The one exception is `content/domain`, which reads
  `artefacts.core.domain.types`.
- A cross-domain call goes through the peer's application layer or a composition root. It
  never goes through the peer's routes.

## Domain map

| Domain | Owns |
| --- | --- |
| `users` | sign-in identity, roles, basic profile |
| `school` | schools, classes, grade levels, academic years, terms, subjects, and the subjects each class takes in a term (`term_class_subjects`) |
| `curriculum` | the NERDC syllabus: topics, subtopics, performance objectives, class sessions, reference materials, and their catalogs |
| `teaching` | teacher workspaces, schemes of work, lesson periods, lesson deliveries |
| `learners` | student identity and stable profile (`student_profiles`) |
| `learner_state` | changing evidence and inferred learner state |
| `assessments` | the class test, exit tickets, classwork, item responses, scoring, synthetic students |
| `expert_content` | textbook packets and records, and objective-to-textbook linkages |
| `artefacts` | the artefact kernel, content specifications, and the artefact kinds (see below) |
| `content` | how each content type is listed, approved and revised, and generation from plans |
| `artefact_revision` | chat-style revision threads on a generated artefact |
| `figures` | TikZ figures, drawn to SVG on the server |
| `attachments` | uploaded provenance images |
| `experiments` | lesson-scoped studies: executions, condition runs, focal cases, packet export |
| `evaluation` | raters, blinded packets, assignments, ratings, source audit, statistics |
| `events` | event telemetry |
| `generation_log` | a log of every LLM generation |
| `tutor` | the runtime tutor |
| `jobs` | who may follow a background job, and what they see |
| `ops` | admin view and control of the job queue and executions |

## Artefacts

| `ArtefactType` | Package |
| --- | --- |
| `lesson_plan` | `artefacts/types/lesson_plan/` |
| `lesson_note` | `artefacts/lesson_note/` |
| `post_class_review_pack` | `artefacts/types/post_class_review_pack/` |
| `diagnostic` (the class test) | `assessments/` |

- Name an artefact kind directly: `artefacts/<kind>/`, beside `artefacts/core/`. Put a new
  kind there.
- `types/` sorts packages by what they are, the directory form of a `services/` bucket. The
  census row `artefact_types_under_a_sorting_dir` in [`code-vocabulary.md`](code-vocabulary.md)
  counts the kinds under it. Story `ART-003` moves them.

- `artefacts/core/` owns the shared lifecycle vocabulary, the `ContentRegistry`, build jobs,
  rendered artefact persistence, and export and download.
- Each content specification is a row in `content_specifications`, one per kind and revision.
  `artefacts/specifications/seed.json` seeds the rows. Each artefact records its revision.

- `artefacts` owns no teaching workflow, no curriculum and no experiment orchestration.
- Each kind owns its own drafting. Do not use `review` as the generic word for an artefact.

## Experiments

- `experiments` owns lesson-scoped studies keyed by workspace and plan version, H1 and H2
  execution, focal-case selection, learner-state snapshots and blinded packet export.
- `experiments/review_pack_study/` holds study behavior only: `conditions/`,
  `condition_runs/`, `h1/`, `h2/`. `tests/test_study_pack_architecture.py` fixes its contents.

- `H1_CONDITION_PROFILES` and `H2_CONDITION_PROFILES` in `conditions/profiles.py` define
  what each condition provides.
- The review-pack product selects no condition by label. It reads the `ConditionProfile` it
  receives.
- `evaluation` owns rubric scoring and statistics. `artefacts` owns the artefact taxonomy.
  `teaching` owns workspace authoring.

## Lesson-plan package

```text
artefacts/types/lesson_plan/
  api/                # routes and HTTP schemas
  application/        # use cases and the role protocols they depend on
  domain/             # plan records and business helpers
  infrastructure/     # repository and ORM models
  drafting/
    application/
      precompute/     # ahead-of-time planning per subtopic, into the file cache
      runtime/        # per-request drafting, validation, diagnostics
    domain/
    infrastructure/dspy/
      modules/        # one module class per task
      signatures/     # one signature module per task
    schemas/          # session_plan.py, the canonical plan contract
    validation/
  deps.py
  jobs.py
```

- `precompute/` builds planning data ahead of time, keyed by subtopic. It writes a file cache,
  never the plan tables. See [`lesson-plan-infrastructure-cache.md`](lesson-plan-infrastructure-cache.md).
- `runtime/` reads the cache. It rebuilds the planning data only when a caller runs the
  precompute path.

- A DSPy module's public `.forward()` reads as three steps: build the prompt input, call DSPy,
  translate the output into domain or schema objects.
- Parsing, fallbacks and identifier construction live in private helpers, not in `.forward()`.

## Canonical Lesson Chain

```text
curriculum side (curriculum domain)
  curriculum_topics
    curriculum_subtopics                 # subtopic_id
      curriculum_performance_objectives
      class_sessions                     # NERDC reference: which subtopic in week N, day M

school side (school domain)
  term_class_subjects                    # a subject a class takes in one term

execution side (teaching, then artefacts)
  teacher_workspaces                     # teacher x term_class_subject
  scheme_of_work                         # per term_class_subject
    lesson_periods                       # the executable teaching unit; subtopic_id FK
      lesson_plans                       # lesson_period_id -> lesson_periods.id
        plan_versions                    # a draft and its revisions
          plan_version_objectives        # derived from session_plan on every write
          artefact_plans, artefacts      # plan_version_id -> plan_versions.version_id
      lesson_deliveries                  # workspace x lesson_period x date, with plan_version_id
```

- `lesson_period` is the attach point for `lesson_plan` and everything downstream.
- `class_session` is curriculum reference data. The plan chain has no foreign key to it.

- The school side records what a school offers in a year. It uses surrogate UUID keys.
- The curriculum side records what the published curriculum carries. The `subject`, `track`,
  `grade` and `term` string columns on `curriculum_topics`, `class_sessions` and
  `reference_materials` reference the `name` column of the matching catalog.
- The two sides have no foreign key between them. They meet through `subtopic_id`.

## Identity and keys

- `learners` owns student identity. Every table names it `student_id` and references
  `student_profiles.student_id`.
- An HTTP contract may name the field `learner_id`. The response builder maps it:
  `learner_id=artefact.student_id`.

- Each entity has a UUID primary key `id` and, usually, a `String(64)` business key with a
  unique index, such as `experiment_id` or `artefact_id`.
- A new foreign key targets the parent's business key when the parent has one.
- Name the constraint `fk_<source_table>_<source_column>`.
- Status columns use `status_enum(...)` from `src/app/db/enums.py` with the domain's enum.

## Shared contracts and typing

- `artefacts/types/lesson_plan/drafting/schemas/session_plan.py` is the canonical lesson-plan
  contract: `SessionPlan`, `SessionPlanContent`, `CurriculumObjectiveRef`. Import it. Make no
  local copy.
- `src/app/shared/session_plan_view.py` holds `SessionPlanView`, a lenient view for code that
  reads a stored plan.

- `src/app/shared/json_types.py` holds the shared JSON aliases.
- Prefer a typed model to a raw JSON payload. Use `Any` only as a last resort.
- Promote a contract to `src/app/shared/` only when two or more domains share it.

## String literals

Extract a string into a constant only when it adds meaning. In order of preference:

1. Replace raw dict access with a typed model or record.
2. For a fixed set of states or kinds, use `Literal`, `StrEnum` or a schema field.
3. For a repeated key in an unavoidable raw payload, use a `Final[str]` constant.

Extract a key constant when the key recurs in one module or crosses files. Also extract it
when it belongs to a persisted contract, or when a typo would fail silently. Keep a one-off
key in a short serializer as a literal.

| Contract scope | Constant lives in |
| --- | --- |
| one module | a module-level constant in that module |
| one subdomain | `types.py` or `constants.py` in that package |
| one domain | the domain's `constants.py` or its canonical schema module |
| two or more domains | `src/app/shared/` |
