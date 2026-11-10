# Backend application boundaries

The callable that HTTP, jobs, CLI scripts and tests invoke, and the size rules for packages,
files, classes and functions.

- Layer meanings: [`domain-architecture-baseline.md`](domain-architecture-baseline.md)
- Transaction ownership: [`persistence-boundaries.md`](persistence-boundaries.md)
- Terms: [`code-vocabulary.md`](code-vocabulary.md)
- Per-route classification for `experiments`: [`experiments-entrypoint-census.md`](experiments-entrypoint-census.md)

## The callable boundary

The reusable operation lives in `application/`. Each transport parses its own envelope, calls
the operation, and renders the result.

```text
HTTP request                     CLI arguments                    job row
     |                                |                                |
     +-------- transport-specific parsing and authentication ----------+
                                      |
                              ApplicationInput
                                      |
                         Use case: Input -> Output
                                      |
                              ApplicationOutput
                                      |
     +---------- transport-specific rendering and error mapping -------+
     |                                |                                |
HTTP response                    stdout/exit code                 recorded job outcome
```

- Give each public operation one immutable input and one explicit output.
- Name the operation for the business verb: `LaunchExecution`, `DraftLessonNote`,
  `PersonaliseReviewPack`. Add no `Service`, `Manager`, `Handler` or `Command` suffix.
- Write a function when the operation has no injected collaborators.
- Write a callable class when the operation needs an injected store, reader, adapter or other role.

```python
@dataclass(frozen=True)
class LaunchExecutionInput:
    experiment_id: str
    hypothesis: Hypothesis
    runtime_snapshot: JsonObject | None
    requested_by: str | None = None


@dataclass(frozen=True)
class LaunchExecutionOutput:
    execution_id: str
    status: ExecutionStatus
    ...


class LaunchExecution:
    def __init__(self, store: ExecutionLaunchStore) -> None:
        self._store = store

    async def __call__(self, request: LaunchExecutionInput) -> LaunchExecutionOutput: ...
```

Source: `src/app/domains/experiments/application/execution_launch.py`.

## Where each contract lives

| Contract | Owner | Examples |
| --- | --- | --- |
| HTTP request and response | `api/` | Pydantic body, query parameters, response model |
| CLI arguments and output | the script's `main()` | argparse options, terminal table, exit code |
| Job envelope | `src/app/infra/jobs/kinds.py` | job kind, handler path, number of runs |
| Use-case input and output | `application/` | frozen dataclass (an application record) |
| Business value or rule | `domain/` | `Hypothesis`, a status transition, a freeze policy |
| External mechanism | `infrastructure/` | SQLAlchemy store, DSPy module, file cache |

Two kinds of immutable record cross these seams:

| Record | Shape comes from | Returned by |
| --- | --- | --- |
| Application record | the operation's contract | a use case |
| Persistence-neutral record | what the read can produce | a store or a reader |

- Both are frozen dataclasses that name no SQLAlchemy, FastAPI or DSPy type.
- `types.py` holds both. "Internal typed record" names that file rule, not a third kind.
- One class may serve both roles when a use case returns a loaded record unchanged.
- An application output carries only plain values that every transport can use.
- A transport that needs more data calls a second application query. It never reads a repository.

### Read-side queries

- A query is a use case: one input, one output, collaborators bound at composition.
- Its output is an application record. `api/` maps that record to a response model.

- `application/` never imports `api/`. The import-linter contract
  `application does not import api transport` enforces this against a shrink-only exemption list.
- One exception: when `to_http_response` would copy field for field, use one type.
  That type lives in `application/`, and `api/` returns it or validates it.

### Errors

- A use case raises its domain's application error, for example `ExperimentApplicationError`
  in `experiments/application/errors.py`.
- `api/` maps the error to an HTTP status. A CLI maps it to a message and an exit code.
- `HTTPException` and exit codes stay in the transport.

## Dependency injection and composition

A composition root builds the use case with its collaborators. The transport receives the
finished callable and passes only the per-call input.

| Transport | Composition root |
| --- | --- |
| HTTP | `api/deps.py`, or the package's `deps.py` |
| Job | the handler that `src/app/infra/jobs/kinds.py` names, which builds through `infrastructure/wiring.py` or `experiments/infrastructure/execution_context.py` |
| CLI | the script's `main()` |
| Test | the test fixture |

```python
# api/deps.py
def launch_execution(
    store: ExecutionLaunchStore = Depends(execution_launch_store),
) -> LaunchExecution:
    return LaunchExecution(store)


# api/routes.py
@router.post("/{experiment_id}/executions")
async def create_experiment_execution(
    experiment_id: str,
    payload: ExperimentExecutionCreateRequest,
    launch: LaunchExecution = Depends(launch_execution),
    ...
) -> ExperimentExecutionResponse:
    execution = await launch(LaunchExecutionInput(experiment_id=experiment_id, ...))
```

- The use case constructs no SQLAlchemy, DSPy or HTTP object.
- Bind collaborators once. Per-call data travels in the input value.
- The import-linter contract `application does not import infrastructure directly` enforces the
  first rule for the packages it lists. Each exemption names the backlog story that deletes it.
- `tests/test_import_contract_ceilings.py` fails when an exemption list grows or when a fix
  leaves its entry behind.
- `tests/test_experiment_entrypoint_boundaries.py` fails an `experiments` transport that
  receives the request session, names a concrete adapter, or takes more than three injected roles.

## Stores and readers

A **store** is the unit of work: one object that owns one transaction and exposes the
capabilities that act inside it.

```python
rating = await store.ratings.find(...)
await store.ratings.stage(rating)
await store.commit()
```

- Only a store has `commit` and `rollback`. A protocol with either one must end in `Store`
  and have both (`test_transaction_capability_is_exposed_only_by_stores`).

- Scope a store to the transaction one workflow commits: `ExecutionLaunchStore`. A store scoped
  to a whole domain collects every method of that domain.
- A store is an application-layer protocol. One concrete adapter may satisfy more than one
  store protocol. No caller sees the concrete type.

- Call it `store`. Public application names never contain `uow`, `unitofwork` or
  `transaction` (`test_public_application_vocabulary_uses_store_not_transaction_jargon`).

A **reader** is the read-only counterpart. It serves **one operation**.

- Name a reader for the operation it serves: `PlanApprovalReader`, not `ExperimentReader`.
- Two operations with similar reads get two readers.

- A read that the write decision depends on must see the write's snapshot. Put it on a store
  capability.
- A read that only supplies reference data comes from a reader injected beside the store.

- A reader carries the `Reader` suffix. A capability reached through a store has a bare name,
  and the property supplies the context: `store.jobs`, `store.ratings`.
- An application protocol has at most ten public members
  (`test_application_protocols_have_a_ten_member_ceiling`).

When three or more readers in one domain declare the same method, their operations share a
collaborator set. Merge the operations into a capability package with one
`<capability>_ports.py`. Do not merge the readers. The census row
`duplicated_reader_signatures` in [`code-vocabulary.md`](code-vocabulary.md) counts these.

Stores and readers return persistence-neutral records, not ORM rows. A pure rule can then live
in `domain/`. The census row `application_signatures_returning_orm` holds the remaining ORM
signatures to a ceiling that only falls.

## How a use case reaches domain and infrastructure

```text
transport adapter
  -> use case
       -> load persistence-neutral records through an injected reader or store
       -> construct domain values
       -> invoke pure domain rules and transitions
       -> stage the resulting state through the store
       -> commit at the business transaction boundary
       -> return an application output
  -> transport response
```

| Layer | Put here |
| --- | --- |
| `domain/` | invariants, allowed transitions, calculations, classifications, policies with no I/O, business values, persistence-neutral records |
| `application/` | which records to load, which rules run and in what order, authorization, transaction timing, coordination of domains and external capabilities, mapping to the output |
| `infrastructure/` | SQLAlchemy statements and ORM mapping, the transaction implementation, the job queue, files, network, DSPy and third-party calls, translation of external payloads |

Move a pure helper from `application/` to `domain/` when it names a stable business rule,
serves callers outside one use case, or protects an invariant. CRUD with no rules gets no
`domain/` layer.

## Package and file granularity

Organize by business domain first, then by layer inside the domain:

```text
domains/experiments/
  api/
  application/
  domain/
  infrastructure/
```

Inside a layer, organize by business capability. A flat directory is correct while its
siblings form one coherent set. Make a capability package when either condition is true:

- three or more modules repeat the same business prefix
- two or more public operations share collaborators, a transaction or a policy vocabulary
  that no other operation uses

A capability package has this shape:

```text
experiments/application/execution_launch/
  launch.py        # LaunchExecution input, output, and callable
  retry.py         # RetryCondition input, output, and callable
  policy.py        # launch-specific preconditions
  launch_ports.py  # ports shared by launch and retry only
```

- Do not create `services/`, `managers/` or `handlers/` directories.
- Declare a port in the module that uses it.

- Name a shared port module for its capability: `launch_ports.py`, `rating_ports.py`.
  `test_every_other_port_module_names_its_capability` enforces the suffix.
- A bare, domain-wide `ports.py` sorts unrelated roles into one bucket.
  `test_only_the_grandfathered_domain_wide_port_buckets_exist` allows only the two that exist
  in `artefacts/core/application/` and `artefacts/types/lesson_plan/application/`.

- No `application/` module or class name contains `helper`
  (`test_application_modules_and_classes_are_not_named_helper`).

### Files

- One file owns one public operation, or one tightly coupled family of operations.
- A protocol, its input and output records, the operation and its private helpers belong
  together.
- Split the file when its operations differ in actor, collaborators, transaction boundary,
  output or reason to change.
- File size is a signal, not the rule. A 70-line pass-through can be an empty layer.
  A 250-line policy table can have one reason to change.

### Classes

Create a class only for one of these reasons:

- it keeps injected collaborators or configuration
- it protects state or a lifecycle
- it is one implementation of a named strategy

Otherwise write a function or an immutable record. A class never groups unrelated methods.

### Functions

- The public function or `__call__` reads as orchestration.
- Each private function owns one decision, transformation or translation, and carries its name.

### Order inside a module

1. module docstring and imports
2. immutable input and output records
3. caller-owned role protocols
4. the public operation
5. private policies, transformations and mappers

Keep a constant beside the rule that gives it meaning. Move it to a shared module only when
sibling operations own the same contract.
