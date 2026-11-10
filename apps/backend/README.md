# Backend

The Plan-to-Tutor API: FastAPI over MySQL, with generation run as background jobs.

```bash
uv run uvicorn app.main:app --reload   # the API, and the job runner inside it
uv run pytest                          # the tests (one run at a time: they share one test database)
```

## Where to look

**`src/app/` is the application.** Everything the API runs is in it.

| Path | What it is |
|---|---|
| `src/app/main.py` | The entry point: prepares the environment and builds the app. |
| `src/app/server.py` | The HTTP app: CORS, static files, error mapping, the router, and MCP at `/mcp`. |
| `src/app/router.py` | Every route, gathered from the domains in one list. |
| `src/app/lifespan.py` | Startup and shutdown: the default school, the job runner, and MCP sessions. |
| `src/app/dspy_setup.py` | The model client and the callbacks on every model call. |
| `src/app/config.py` | Every tunable and path, in code. Only secrets come from the environment. |
| `src/app/domains/<domain>/` | One folder per domain: `api/` (routes), `application/` (use cases), `domain/` (rules), `infrastructure/` (database, model calls). |
| `src/app/infra/` | Shared plumbing: the job queue, progress events, model clients. |
| `src/app/db/` | Engine, sessions and the ORM model registry. |
| `src/app/shared/` | Small types and helpers the domains share. |
| `src/app/static/` | Local copies of textbook figures, served at `/static`. |

**Everything else supports the application:**

| Path | What it is |
|---|---|
| `tests/` | The test suite. |
| `migrations/` | Changes to the database: `schema/` (Alembic, `uv run alembic upgrade head`) and `data/` (data changes, each a module run on deploy or by hand). |
| `scripts/` | One-off command-line tools: seeding, imports, builds. |
| `experiments/` | The research harnesses behind the thesis; their runs are versioned by DVC (`experiments/README.md`). |
| `docs/` | Design notes: boundaries, vocabulary, the generation call stack. |
