# AI for Good Sandbox Hackathon – Tosin Amuda – Teacher Agent

Teacher Agent is an education agent grounded in the Nigerian curriculum, with teacher approval. Entry to the ITU AI for Good Lab Hackathon (UAE, 2026). A teacher-in-the-loop agent drafts a JSS1 mathematics lesson plan and the class materials made from it, from the NERDC curriculum. Nothing reaches a learner until the teacher approves it.

The code and documents inside still use the project's working names, Plan-to-Tutor and LPCG.

The rest of this repository is the full Teacher Agent application, copied from the project's `main` branch, without its git history and without `apps/backend/experiments/` (the study's analysis code and outputs, which the hackathon does not use). Code that imports that folder, such as the study tests and the study-import migration, does not run in this copy. This folder holds what is specific to the hackathon: this README and the dataset, with policy and use-case data kept apart. The technical report (submitted by email) explains the use case, the mapping and the error scenarios.

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

## Dataset (`Dataset/Nigeria/`)

Laid out like ITU's `Sandbox_Training` dataset: the policy documents and the use-case data are separate.

| Folder | Holds |
|---|---|
| `Dataset/Nigeria/PolicyData/` | The knowledge base: 10 official policy, law, strategy and curriculum documents in ITU's sector folders (`01_AI_Strategy_and_Governance`, `02_Data_Protection`, `12_Education`), with `Refs.md` giving each one's issuer, URL, how it was checked and its SHA-256. The ITU reference code ingests this folder. Ingestion was not run for this submission. |
| `Dataset/Nigeria/UsecaseData/ng-jss1-math-curriculum/` | The use case's own data: the NERDC JSS1 mathematics curriculum as 78 atomic objectives, and the Lagos State scheme of work that paces it (CC BY 4.0). |
| `Dataset/Nigeria/UsecaseData/ng-jss1-math-textbook-linkage/` | Siyavula's open textbook *Mathematics JSS-1* as 1,500 records, each linked to a curriculum objective (CC BY 3.0 for the textbook, CC BY 4.0 for the linkage; see its `LICENSE.md`). |

The use-case data are copied unchanged.

## Not included

Git history, secrets, and the rater and learner documents.
