# Teacher Agent: hackathon material

## Dataset

| Folder | Holds |
|---|---|
| [`Dataset/Nigeria/PolicyData/`](Dataset/Nigeria/PolicyData/Refs.md) | The knowledge base: 10 official documents. `Refs.md` lists each source. |
| [`Dataset/Nigeria/UsecaseData/`](Dataset/Nigeria/UsecaseData/) | The curriculum (78 objectives), the scheme of work, and the textbook (1,500 linked records). |

## ITU-T Y.3172 nodes in the code

Paths are under `apps/backend/src/app/domains/`.

| Node | Here | Code |
|---|---|---|
| SRC | Curriculum, textbook and teacher documents | `content_engine/infrastructure/documents.py` |
| PP | Schema check on every part before it is stored | `content_engine/infrastructure/checker.py` |
| M | The agent drafts one curriculum objective at a time | `content_engine/application/drafting.py` |
| P | Teacher approval gates | `content/application/review.py`, `content_engine/application/plan_review.py` |
| D | A learner reads only an approved note | `artefact_revision/application/` |
| SINK | Teacher review view | `content_engine/application/draft_view.py` |
| MLFO | Agent runs queued as jobs | `content_engine/jobs.py` |
| ML intent | Each material type is a JSON specification and a skill | `/plugins/` |

## Audit trail

- Every agent call can be logged: `generation_log/`.
- Role-based access: `apps/backend/src/app/shared/authz.py`.
