# Teacher Agent

Entry to the ITU AI for Good Lab Hackathon (UAE, 2026). A teacher-in-the-loop agent drafts a JSS1 mathematics lesson plan and the class materials made from it, from the Nigerian NERDC curriculum. Nothing reaches a learner until the teacher approves it. The code and documents still use the project's working names, Plan-to-Tutor and LPCG.

**Start here:** [`hackathon/README.md`](hackathon/README.md) maps each ITU-T Y.3172 pipeline node to its code and lists the audit trail.

## Where to look

| What | Where |
|---|---|
| Policy, law and strategy documents (the knowledge base) | [`hackathon/Dataset/Nigeria/PolicyData/`](hackathon/Dataset/Nigeria/PolicyData/Refs.md) |
| The use case's own data: curriculum, scheme of work, textbook, linkage | [`hackathon/Dataset/Nigeria/UsecaseData/`](hackathon/Dataset/Nigeria/UsecaseData/) |
| The agent that drafts and checks content | `apps/backend/src/app/domains/content_engine/` |
| Teacher approval of plans and materials | `apps/backend/src/app/domains/content/` |
| The trace of every agent call (off by default) | `apps/backend/src/app/domains/generation_log/` |
| Role-based access | `apps/backend/src/app/shared/authz.py` |
| Material types as plugins: a JSON specification and a written skill for each | `plugins/` |
| The teacher web app | `apps/frontend/` |
| Server set-up | `deploy/ansible/` |

## Stack

A Turborepo monorepo with two apps and one database.

| Part | Stack |
|---|---|
| `apps/frontend` | Vite, React, TanStack Query, Tailwind, TipTap, KaTeX |
| `apps/backend` | FastAPI, async SQLAlchemy, Alembic, DSPy, litellm, Casbin |
| Database | MySQL |

## Running it

This copy is for reading and review. It does not run end to end: the set-up script `apps/backend/scripts/seed_all.py` fetches data from outside this repository and calls study code that was removed (`apps/backend/experiments/`). The data it needs is included under `hackathon/Dataset/Nigeria/UsecaseData/`.

A working instance of the full system exists. A demo is available if the team is shortlisted.
