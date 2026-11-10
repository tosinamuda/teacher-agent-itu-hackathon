# Textbook–Curriculum Linkage

How textbook records reach a lesson. A curator links each atomic objective (AO) to textbook records by hand. The lesson-plan drafter reads those links. A revision note reads the textbook records that its plan cites. The `expert_content` domain holds the textbook and the links.

Terms: [glossary.md](glossary.md). Tables: [data-model.md](data-model.md).

## Flow

```text
textbook records ─┐
                  ├─▶ manual AO linkage ─▶ lesson-plan drafting ─▶ plan references ─▶ revision note evidence
curriculum AOs ───┘   (curator, JSON)      (manual_linkage or       (record IDs)        (textbook or both)
                                            curriculum_only)
```

| Stage | Who | Input | Output |
|---|---|---|---|
| Linkage | a curator | textbook records and the AOs of one subtopic | one JSON file per subtopic |
| Seed | `seed_ao_textbook_linkage.py` | the JSON files | the `ao_textbook_*` tables |
| Plan drafting | the lesson-plan drafter | the subtopic's linked records | a plan that cites record IDs |
| Revision note | the revision-note generator | the plan's cited records | evidence for each step |

## Manual linkage

- A curator writes the links. No model or embedding chooses them.
- The seed script validates each file against the schema. It checks that every subtopic and record exists. It reports and skips a row that fails.
- The source files are in `dataset/processed/ao_textbook_linkage/manual/`.

```
AoTextbookLinkage          one per subtopic; status: mapped | needs_review | no_records; shared_foundation_record_ids
├─ AoTextbookObjectiveLink one per AO; curriculum_objective_id, bloom_level, step_blueprint, practice_record_ids, assessment
└─ AoTextbookRecordLink    one per AO and record; role, method, rationale, link_order
```

| Field | Values |
|---|---|
| `AoTextbookRecordLink.role` | `foundation`, `instruction`, `worked_example`, `exercise` |
| `AoTextbookRecordLink.method` | `rule_type`, `rule_heading`, `judgment` |
| `AoTextbookObjectiveLink.assessment` | a question and expected answer from a textbook exercise, or none |

### Coverage

Measured on the source files and on the dev database on 2026-09-25:

| Count | Value |
|---|---|
| Subtopic files | 78 |
| Atomic objectives | 158 |
| AOs with at least one record link | 136 |
| AOs with no record link | 22 |
| Record links | 997 |
| AOs with a reused textbook assessment | 111 |

The AOs with no link cover topics that the textbook does not teach. Examples are pie charts, histograms, complementary angles, the angle sum of a triangle, and significant figures.

## Lesson-plan drafting

The drafter picks a grounding mode for each subtopic:

| Mode | When | What the drafter reads |
|---|---|---|
| `manual_linkage` | the subtopic has linked records | the linked records, shared foundation records first, then by AO and link order |
| `curriculum_only` | the subtopic has no linkage, or no usable records | the curriculum objectives alone |

- In `manual_linkage` mode, the curated links set each AO's knowledge components, worked examples and assessment.
- The plan cites each record it uses as a reference that ends in the record ID, for example `"Chapter 2: … (ch02-b029)"`.

## Revision-note evidence

- The generator resolves each plan reference to its record in `textbook_records`. It reads `prompt_text`, then `content_text`, then `retrieval_text`.
- The teacher's choice of expert sources decides whether these records reach the model. See [revision-note-generation.md](revision-note-generation.md).
- The generator does no search. Only the records that the plan cites can reach a revision note.

## Textbook records and figures

`TextbookRecord` fields that generation reads:

| Field | Meaning |
|---|---|
| `record_id` | the key that plan references end in |
| `record_type`, `heading_path`, `chapter_id` | where the record sits in the book |
| `prompt_text`, `content_text`, `retrieval_text` | the record's text |
| `asset_refs` | the record's images: `src`, `alt`, `ordinal`, `asset_type` |
| `primary_subtopic_id`, `link_status` | the curriculum subtopic, and `linked`, `ambiguous` or `unlinked` |

### Image cache

- The backend keeps a copy of the textbook images in `apps/backend/src/app/static/figures/`. It serves them at `/static/figures/<file>`.
- `captions.json` in the same folder holds a written caption for each of the 57 images.
- The frontend rewrites a textbook image URL to the local copy. If the copy is missing, it loads the remote URL.

### Figures in generated text

- A `visual` block carries its caption as written.
- The lesson-plan drafter refers to an image in general terms, such as "the chart below". It does not describe what it cannot see.
- The revision-note writer cites a figure by its `fig-NN` label.

## Code

| Concern | Path |
|---|---|
| Linkage models | `apps/backend/src/app/domains/expert_content/models/ao_textbook_linkage.py` |
| Textbook models | `apps/backend/src/app/domains/expert_content/models/textbook.py` |
| Linkage seed | `apps/backend/scripts/seed_ao_textbook_linkage.py` |
| Linkage source files | `dataset/processed/ao_textbook_linkage/manual/` |
| Grounding mode and linked records | `apps/backend/src/app/domains/artefacts/types/lesson_plan/infrastructure/repository.py` |
| Curated planning | `apps/backend/src/app/domains/artefacts/types/lesson_plan/drafting/application/precompute/curated_planning.py` |
| Reference resolution | `apps/backend/src/app/domains/expert_content/application/excerpt_resolver.py` |
| Figure URL rewrite | `apps/frontend/src/shared/utils/figure-url.ts` |
