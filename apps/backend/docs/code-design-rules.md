# Code design rules

Nine rules for when a seam, a layer, a module or a constant earns its place, and the check
or tool that holds each one. The layer taxonomy lives in
[`domain-architecture-baseline.md`](domain-architecture-baseline.md). The callable boundary
lives in [`application-boundaries.md`](application-boundaries.md).

Abstraction and decoupling pay in one currency: change. Abstract to absorb a variation you
can name, or to invert a dependency on something volatile. Decouple so that a change in one
place does not force changes elsewhere. Structure that buys neither is ceremony.

## Rule 1: abstract across a named axis, or not at all

- A seam hides a named variation, or it inverts a dependency on something volatile.
  "We might swap it later" does not count.

- A caller-owned `Protocol` with one SQLAlchemy implementation is correct. It exists because
  `application/` must not import `infrastructure/`.
- `models/`, `schemas/` and `types.py` change for three independent reasons: persistence
  shape, wire contract and internal record. That justifies three representations.

- A second copy of a Pydantic schema names no axis. Import the canonical one, such as
  `session_plan.py`.
- Apply an abstraction that exists. A status column uses its domain enum through
  `status_enum`, and code compares enum members, not string literals:

```python
status: Mapped[ExecutionStatus] = mapped_column(
    status_enum(ExecutionStatus, name="execution_status"),
    index=True,
)
```

**Check.** State the variation the seam hides, or the dependency it inverts, in one sentence.
If you cannot, inline the seam.

## Rule 2: dependencies point toward stability, without cycles

- Domain rules, status enums and typed records are the stable center. SQLAlchemy, DSPy and
  LiteLLM are volatile, and code that uses them depends inward.
- If package A imports B and B imports A, they are one module. `make pylint` fails on
  `cyclic-import`.

- The import-linter contracts fix the direction. The list is in
  [`domain-architecture-baseline.md`](domain-architecture-baseline.md#dependency-contracts).
- Shapes you do not control, such as ORM rows and external payloads, stop at the boundary.
  Map them into your own records there.

**Check.** Can each layer carry full type annotations without a peer domain's ORM import?
If not, the boundary leaks.

## Rule 3: every module owns a decision

A module earns its place when it makes a choice its caller does not make:

- it enforces an invariant
- it selects a strategy
- it owns a transaction boundary
- it translates between two representations
- it manages a resource's lifecycle

A body that is one forwarding call owns nothing. Inline it.

The precedent is `H1_CONDITION_PROFILES` and `H2_CONDITION_PROFILES` in
`experiments/review_pack_study/conditions/profiles.py`. One data registry owns the dispatch
decision, and no `if hypothesis == H1` chain repeats it.

After you split a module, run the verb test again on each part. A part that only loads from a
repository and returns has moved the work, not decomposed it.

**Check.** Describe the module's job in one sentence whose verb is not *calls*, *forwards* or
*delegates*. A pass-through fails the sentence. A god module needs more than one sentence.

## Rule 4: collaborators arrive by injection

- A module declares what it needs and receives it. It never constructs or imports its
  collaborators.
- `Depends()` injects at the HTTP edge. Constructors carry injection below it. `deps.py` and
  `infrastructure/wiring.py` hold the wiring.

- A use-case constructor takes its collaborators as required arguments. A default such as
  `repo or ConcreteRepo()` would import `infrastructure/`, which the import-linter contract forbids.
- Keep volatile libraries behind one adapter. `src/app/infra/dspy_lm.py` builds every DSPy LM,
  and `src/app/infra/llm_models.py` declares each model's quirks.

- Separate the ports, injected once, from the per-call data, passed in one input dataclass.
- Never call another object's private members.

**Check.** Can a unit test construct the use case with fake ports, no database session, no
FastAPI and no DSPy? `tests/test_experiment_entrypoint_boundaries.py` holds the `experiments`
transports to this.

## Rule 5: one unit per responsibility

- Add no pass-through layers. A Controller, Service, Manager, Processor and Helper staircase
  launders one call through five names.
- Name each module for its job: `objective_atomizer`, `kc_extractor`, `assessment_designer`.
- Collapse no set of decisions into one god function.

| Gate | Limit | Command |
| --- | --- | --- |
| ruff `C901`, `PLR0912`, `PLR0915` | `max-complexity = 10` | `make lint` |
| xenon | no block worse than C, no module worse than B, average A | `make complexity` |

- `[tool.ruff.lint.per-file-ignores]` in `pyproject.toml` names five files with known complex
  functions. Add no file to that list.
- `h1_worksheet_pdf.py` and `audit_pack_pdf.py` in `evaluation/application/` hold the frozen
  reportlab fallback. Fix bugs there, and add features to the WeasyPrint renderer.

**Check.** Can you name each layer for a responsibility, not a position? Does each unit stay
inside the gates?

## Rule 6: fit the structure to each subdomain

- Each layer means the same thing in every domain. How many layers a domain has depends on
  its rules.
- Reference and CRUD domains, such as `users` and most of `school` and `curriculum`, stay
  thin: a route, a repository, and no `domain/` layer when there are no rules.
- `artefacts` and `experiments` carry lifecycles, condition runs, focal cases and blinded
  packets. They earn the full set of layers.

- The identity and reference domains are thin in orchestration and strict in schema, because
  every other domain references them.
- One concept has one owner. `learners` owns student identity, and every other table
  references `student_profiles.student_id`.
- Before a migration adds a foreign key, count the rows that break it. MySQL rejects a
  constraint that the existing data does not satisfy.

**Check.** Count the invariants and state transitions in the subdomain. Near zero means CRUD
over a repository. More means a domain model, ports and perhaps a validation package.

## Rule 7: view queries never write

The application layer has two shapes. Keep one shape per file.

| Shape | Job | Writes |
| --- | --- | --- |
| Command | one mutation: load, change, persist | yes |
| View query | assemble one output from many tables for one consumer | never |

- A view query calls no `repository.save_*`, `update_*`, `delete_*` or `set_*`.
- A view query calls no `db.add()`, `db.delete()` or `db.flush()`.
- `tests/test_read_write_seam.py` checks each file in `VIEW_SERVICE_FILES`. Add each new view
  file to that list.
- An operation that must write is a command. Name it for its business verb and keep it off
  the list.

## Rule 8: `api/` imports no ORM model at runtime

- `api/` converts HTTP to application records and back.
- A route imports an ORM class only under `if TYPE_CHECKING:`.
  `tests/test_api_does_not_import_models.py` walks each `api/` file and fails a runtime import.

- A route reaches another domain through that domain's application layer. Only a composition
  root such as `api/deps.py` names a peer's `infrastructure/`.
- The contract `api transport does not directly import peer-domain code` covers
  `curriculum.domain` only. Review holds the rest of this rule.

## Rule 9: paths name stories, and symbols name operations

- Repeated filename prefixes mean a missing package. `h1_experiment.py` and `h1_outcomes.py`
  as siblings become `h1/experiment.py` and `h1/outcomes.py`.
- Name a public class for the operation it performs: `GenerateBaseReviewPack`,
  `PersonaliseReviewPack`, `CritiqueSections`. Framework terms stay at the framework boundary.

- Create no `services/`, `managers/`, `handlers/` or `repositories/` directory to sort files by
  shape.
- In review-pack generation, `infrastructure/dspy/` is the model boundary. Inside it,
  `contracts/` holds what the model must return and `tools/` holds what an agent may do.

- `src/app/domains/experiments/` is production code. The top-level `experiments/` directory is a
  research harness. The harness may import production code. Production never imports the harness.

**Check.** Can you explain the siblings at each directory level as one coherent set?
`tests/test_study_pack_architecture.py` holds the review-pack product to its names and its
boundary with the study.

## Enforcement

`make quality` runs the tool gates. `uv run pytest -m architecture` runs every structural test.

| Rule | Tool or test |
| --- | --- |
| 1, 4 | import-linter `application does not import infrastructure directly`, `mypy` |
| 2 | `pylint` cyclic-import, import-linter contracts, census row `application_signatures_returning_orm` |
| 4 | `tests/test_experiment_entrypoint_boundaries.py` |
| 5 | ruff complexity rules, xenon |
| 7 | `tests/test_read_write_seam.py` |
| 8 | `tests/test_api_does_not_import_models.py`, import-linter `api transport does not directly import peer-domain code` |
| 9 | `tests/test_study_pack_architecture.py`, `tests/test_code_vocabulary_census.py` |

Rule 3 (name the verb), Rule 6 (count the invariants) and the naming half of Rule 9 need a
reviewer.
