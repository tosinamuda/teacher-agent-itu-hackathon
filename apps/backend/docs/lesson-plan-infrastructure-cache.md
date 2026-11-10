# Lesson-plan infrastructure cache

`scripts/build_lesson_infrastructure.py` plans the lesson infrastructure for curriculum
subtopics ahead of time. It writes the result to a file cache. The database holds no part of it.

- The unit of work is one subtopic.
- A batch run is a loop over all subtopics.
- The LLM planning path of lesson drafting reads the same cache format. The manual-linkage path uses curated planning and skips the cache.

## Contents

Each subtopic gets one directory, `<cache root>/<slugified subtopic_id>/`:

```text
<subtopic>/
  metadata.json                  # the cache key (see Validity)
  atomic_objectives.json
  combined_kc_plan.json
  lesson_structure.json          # merged objectives, blueprints, KCs
  lesson_assessment_items.json
  step_evidence_plans.json
  ao-NN/                         # one per atomic objective
    kc_decomposition.json
    assessment_items.json
    verification.json            # violations for this objective
```

A script run also writes `quality-report.txt` and `summary.json` at the cache root.

## Cache root

The cache root is `CONFIG.lesson_plan.infrastructure_cache_dir` in `src/app/config.py`:
`apps/backend/.cache/lesson-plan-infrastructure`.
The script writes there, and the drafting runtime reads from there.
Use `--output-dir` to make the script write somewhere else.

## Inputs

| Option | Default | Content |
| --- | --- | --- |
| `--topics` | `dataset/processed/curriculum/jss1_topics_enriched.json` | Enriched curriculum topics |
| `--scheme` | `dataset/processed/scheme-of-work/jss1_scheme.json` | Scheme of work |
| `--records` | `dataset/processed/textbook/jsonl/linked/records.jsonl` | Linked textbook records |
| `--subtopic-id` | none | Only this subtopic |
| `--report-path` | `<output-dir>/quality-report.txt` | Text quality report |
| `--summary-path` | `<output-dir>/summary.json` | JSON summary, one row per subtopic |

- The default paths are relative to the repository root. `PROJECT_ROOT`, `CURRICULUM_PATH`, `SCHEME_PATH` and `TEXTBOOK_LINKED_ROOT` override them.
- The script caches under the model the drafting runtime uses (`active_model_name()`), so the runtime reads what the script writes.

## Run

```bash
cd apps/backend
uv run python scripts/build_lesson_infrastructure.py --subtopic-id <subtopic_id>  # one subtopic
uv run python scripts/build_lesson_infrastructure.py                              # all subtopics
```

The script prints the quality report and the path of `summary.json`.

## Validity

`InfrastructureArtifactCache.get()` returns an entry only when all of these match `metadata.json`:

| Key | Changes when |
| --- | --- |
| `subtopic_id` | A different subtopic is requested. It is the directory name. |
| `infrastructure_version` | A developer bumps `INFRASTRUCTURE_VERSION` in `cache.py` (now `v2`). Bump it when a cached pass changes its output shape. |
| `textbook_hash` | The textbook records for the subtopic change. |
| `curriculum_hash` | The curriculum objectives, evaluation guide, entry behaviour, instructional materials, topic key or subtopic change. |
| `model_name` | The planning model changes. |

- A missing required file is also a miss.
- `invalidate(subtopic_id)` deletes one entry. `invalidate_all()` deletes every entry.

## Quality report

The report lists every invalid subtopic. Violation codes:

| Code | Meaning |
| --- | --- |
| `zero_linked_textbook_records` | The subtopic has no linked textbook records. The script plans nothing for it. |
| `source_id_not_found` | A KC cites a supporting record id that is not in the textbook records. |
| `bloom_coverage_gap` | No taught KC reaches the Bloom level of the atomic objective. |
| `type_inconsistency` | A KC type does not agree with the support types of its records. |
| `dag_cycle` | The prerequisite graph has a cycle. |

## Code

| Part | Path |
| --- | --- |
| Script | `scripts/build_lesson_infrastructure.py` (`build_subtopic_infrastructure`) |
| Planning package | `src/app/domains/artefacts/types/lesson_plan/drafting/application/precompute/` |
| Cache | `precompute/cache.py` (`InfrastructureArtifactCache`) |
| Runtime caller | `src/app/domains/artefacts/types/lesson_plan/drafting/infrastructure/dspy/modules/generator.py` |
