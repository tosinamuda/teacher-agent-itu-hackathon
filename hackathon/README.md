# AI for Good Sandbox Hackathon – Tosin Amuda – Teacher Agent

Teacher Agent is an education agent grounded in the Nigerian curriculum, with teacher approval. Entry to the ITU AI for Good Lab Hackathon (UAE, 2026). A teacher-in-the-loop agent drafts a JSS1 mathematics lesson plan and the class materials made from it, from the NERDC curriculum. Nothing reaches a learner until the teacher approves it.

The code and documents inside still use the project's working names, Plan-to-Tutor and LPCG.

The rest of this repository is the full Teacher Agent application, copied unchanged from the project's `main` branch (without its git history). This folder holds what is specific to the hackathon: this README, the knowledge base and the seed data. The technical report (submitted by email) explains the use case, the mapping and the error scenarios.

## Features

- Drafts a lesson plan and class materials one curriculum objective at a time.
- Checks every part against a schema before it is stored.
- Two teacher approval gates: nothing reaches a learner until the teacher approves it.
- A trace of every agent call and role-based access (the audit trail).
- Each material type is a plugin: a JSON specification and a written skill.

## Where each ITU-T Y.3172 node is in the code

Paths are under `apps/backend/src/app/`.

| Node | What it does here | Code |
|---|---|---|
| SRC | Curriculum, textbook and teacher documents as input | `domains/content_engine/infrastructure/documents.py`, `domains/content_engine/application/plan_outline.py` |
| PP | Every part the agent writes is checked against its schema before it is stored | `domains/content/revision_note_parts.json`, `domains/content/revision_note_learner_parts.json`, `domains/content/class_test_parts.json`, `domains/content_engine/infrastructure/checker.py` |
| M | The tool-using agent that drafts one curriculum objective at a time | `domains/content_engine/application/drafting.py`, `domains/content_engine/application/draft_tools.py`, `domains/content_engine/infrastructure/harness/` |
| P | Teacher approval gates, with the checks shown at approval | `domains/content/application/review.py`, `domains/content/infrastructure/review.py`, `domains/content_engine/application/plan_review.py`, `domains/content_engine/application/held_checks.py` |
| D | A learner reads only an approved note | `domains/artefact_revision/application/` |
| SINK | Teacher review view and learner reading, fed by the stored draft state | `domains/content_engine/application/draft_view.py`, `domains/content_engine/api/routes.py` |
| MLFO | Long agent runs are queued as jobs | `domains/content_engine/jobs.py`, `domains/content/jobs.py` |
| ML intent (declarative specification) | Each material type is a JSON specification plus a skill; a new type is a plugin | `/plugins/*/`, `docs/artefact-plugins.md`, `docs/content-types.md` |

## Auditability

- **Trace of every agent call:** `domains/generation_log/`. Off by default (`CONFIG.log_model_calls`), because the log grows with every call.
- **Who may do what:** role-based access with Casbin, `shared/authz.py` and `shared/auth_model.conf`.
- **Plugins:** `plugins/` holds the specification and the written skill for each material type (lesson plan, lesson note, class test, slide deck, revision note).

## Data (`hackathon/data/`)

The seed data the agent reads from, released with the thesis as two of four open datasets (copied unchanged, each with its README, PROVENANCE.json and licence):

| Folder | Holds | Licence |
|---|---|---|
| `hackathon/data/ng-jss1-math-curriculum/` | NERDC JSS1 mathematics curriculum as 78 atomic objectives, and the Lagos State scheme of work that paces it | CC BY 4.0 |
| `hackathon/data/ng-jss1-math-textbook-linkage/` | Siyavula's open textbook *Mathematics JSS-1* as 1,500 records, each linked to a curriculum objective | CC BY 3.0 (textbook), CC BY 4.0 (linkage); see `LICENSE.md` |

## Not included

Git history, secrets and the rater and learner documents. Those documents are fetched at set-up from the gated Hugging Face datasets `tosinamuda/ng-jss1-math-{lesson-plans,alignment-ratings}` and are ignored by git. The two datasets above are also on Hugging Face: `tosinamuda/ng-jss1-math-{curriculum,textbook-linkage}`.

## Knowledge base

The policy and law documents used for the hackathon knowledge base are listed in `knowledge-base/README.md` and sent with the submission.
