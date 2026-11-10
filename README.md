# Plan-to-Tutor: an education agent grounded in the Nigerian curriculum, with teacher approval

Entry to the ITU AI for Good Lab Hackathon (UAE, 2026). A teacher-in-the-loop agent drafts a JSS1 mathematics lesson plan and the class materials made from it, from the NERDC curriculum. Nothing reaches a learner until the teacher approves it.

This repository is an **excerpt** of the full application, limited to the parts the judging criteria ask about. It is not runnable on its own: it imports modules that are not included. The technical report (submitted by email) explains the use case, the mapping and the error scenarios.

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

## Not included

Study data, rater and learner records, deployment files, secrets, the front end and the full database layer. The four curriculum datasets are on Hugging Face (public, manual-approval access): `tosinamuda/ng-jss1-math-{curriculum,textbook-linkage,lesson-plans,alignment-ratings}`.

## Knowledge base

The policy and law documents used for the hackathon knowledge base are listed in `knowledge-base/README.md` and sent with the submission.
