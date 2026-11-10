# Backend persistence boundaries

How data access and transactions cross the layers under `src/app/domains/`. Store and reader
naming lives in [`application-boundaries.md`](application-boundaries.md#stores-and-readers).

## Rule

A use case receives persistence **capabilities**: readers and stores. It never receives an
`AsyncSession`.

```text
composition root (api/deps.py, a job's wiring)
  -> open a SQLAlchemy-backed store on one session
  -> pass a reader or the store to the use case
  -> the use case decides when the business transaction commits
  -> the store commits; on error, the store's context rolls back
```

## Read-only use cases receive readers

A read-only use case receives the smallest protocol that describes its reads. It gets no
`commit` and no `rollback`.

```python
class PlanApprovalReader(Protocol):
    async def get_plan_version(self, plan_version_id: str) -> LaunchPlanRecord | None: ...


async def ensure_plan_is_approved(reader: PlanApprovalReader, experiment: Experiment) -> None: ...
```

Source: `src/app/domains/experiments/application/launch_policy.py`.

## Transactional use cases receive a store

An operation whose writes must be atomic receives a store. The store exposes only the
capabilities in that transaction, plus `commit` and `rollback`.

```python
class ExecutionLaunchStore(Protocol):
    @property
    def experiments(self) -> LaunchExperiments: ...

    @property
    def executions(self) -> LaunchExecutions: ...

    @property
    def jobs(self) -> LaunchJobs: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
```

Source: `src/app/domains/experiments/application/launch_ports.py`.

The use case decides **when** to commit. The store decides **how**.

- A store context rolls back on error and never commits on its own. If nobody calls
  `commit`, nothing persists. `tests/test_experiment_persistence_boundaries.py` holds
  `open_experiment_store` to this.
- Opening a store opens the transaction. H1 opens two stores, so that minutes of model calls
  hold no transaction open.

## Background jobs

A job is a row in the MySQL `jobs` table (`src/app/infra/jobs/models.py`).

- Queue a job in the same transaction as the change that asks for it: `store.jobs.add(...)`,
  or `JobQueue.add` on the request session (`src/app/infra/jobs/deps.py`).
- The job and the change then commit together, or neither commits.
- Use `JobQueue.submit` only when the job is the whole transaction.
- Use `JobQueue.ensure` to follow an unfinished job of the same kind and subject.

## Repositories and ports

- A repository runs reads and stages writes. It never commits a transaction that a wider use
  case owns. `tests/test_experiment_repository_commit_census.py` holds `ExperimentRepository`
  to this.
- Some repositories outside `experiments` commit. Do not copy them.

- A port describes one caller role. It never mirrors a table, an ORM repository or a domain
  directory.
- Group the methods that change for the same use case.
- Write no protocol or class per method.
- One SQLAlchemy adapter may satisfy many role protocols. Split the adapter only when its
  persistence duties, read model or resource lifecycle differ.

The test is whether a caller can name the one role it depends on without gaining unrelated
capabilities.

## Boundary constraints

- `AsyncSession`, SQLAlchemy statements, `commit`, `flush` and `rollback` stay in composition
  roots and `infrastructure/` adapters.
- Application and domain signatures use internal records, identifiers and domain values.
  The census row `application_signatures_returning_orm` holds ORM-row signatures to a
  falling ceiling.

- Writes in two domains that must be atomic go through capabilities bound to one store and
  one session. A use case never passes the session across a domain boundary.
- FastAPI dependency functions and job wiring are composition roots. Routes and job handlers
  receive finished readers and stores.
