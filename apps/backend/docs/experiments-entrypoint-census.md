# Experiments entrypoint census

This census lists every entrypoint into the experiments domain and the use case it calls.

- The rule: [`application-boundaries.md`](application-boundaries.md).
- The guard: `tests/test_experiment_entrypoint_boundaries.py`.
- The guard baselines are exact sets. Classify a new entrypoint here in the same change that adds it.
- When you fix a gap, remove it from the baseline in the same change.

## Summary

- 38 HTTP handlers and 3 job kinds start an experiments use case.
- One use case, `LaunchExecution`, has the operation shape (see [Operation shape](#operation-shape)).

| Gap | Count | Meaning |
| --- | --- | --- |
| session | 7 | The handler receives the request session. The transaction boundary is outside the operation. |
| assembly | 3 | The handler receives four or more roles and sequences the use case itself. |
| dispatch | 4 | The handler queues a job from its body. It calls no use case. |
| transport-only | 2 | The handler needs no use case. It returns static configuration or relays a progress channel. |

## Scripts and harnesses

No script or research harness calls an experiments use case. These files import
`app.domains.experiments.infrastructure` directly:

- `experiments/p1_evidence_prompt/runner.py`
- `experiments/p1_prompt_eval/dataset.py`
- `scripts/seed_jss1_curriculum.py`
- `experiments/study_import/`: `importer.py`, `runs.py`, `transcript_rows.py`, `withdraw.py`. They write the rows of the concluded study.

## The census

The Gap column uses the four codes from the summary table.

| Route or job kind | Handler | Use case | Gap |
| --- | --- | --- | --- |
| `POST /experiments/investigations` | `create_investigation` | `create_investigation_command` | |
| `GET /experiments/investigations` | `list_investigations` | `InvestigationApplicationService.list_investigations` | |
| `GET /experiments/investigations/{investigation_id}` | `get_investigation` | `InvestigationApplicationService.get_investigation` | |
| `POST /experiments/investigations/{investigation_id}/end` | `end_investigation` | `end_investigation_command` | |
| `GET /experiments/workspaces` | `list_experiment_workspaces` | `list_workspace_options` | |
| `GET /experiments/workspaces/{workspace_id}/lessons` | `list_workspace_lessons` | `list_workspace_lesson_options` | |
| `GET /experiments/workspaces/{workspace_id}/lessons/{lesson_period_id}/approved-versions` | `list_workspace_lesson_versions` | `list_workspace_lesson_approved_versions` | |
| `POST /experiments` | `create_experiment` | `ExperimentApplicationService.create_experiment` | session |
| `POST /experiments/{experiment_id}/plan` | `author_experiment_plan` | `ExperimentApplicationService.check_plan_authoring` | session |
| `POST /experiments/{experiment_id}/plan/manual` | `author_experiment_plan_manual` | `ExperimentApplicationService.author_experiment_plan_manual` | session, assembly |
| `POST /experiments/{experiment_id}/plan/reuse` | `reuse_experiment_plan` | `ExperimentPlanReuse` | |
| `POST /experiments/{experiment_id}/plan/freeze` | `freeze_experiment_plan` | `ExperimentApplicationService.freeze_experiment_plan` | session, assembly |
| `POST /experiments/{experiment_id}/review-note` | `create_experiment_review_note` | `ExperimentApplicationService.create_review_note` | session, assembly |
| `POST /experiments/{experiment_id}/classwork/manual` | `author_experiment_classwork_manual` | `ExperimentApplicationService.author_experiment_classwork_manual` | session |
| `GET /experiments` | `list_experiments` | `ExperimentListQuery.list_experiments` | |
| `PUT /experiments/{experiment_id}/focal-learners` | `update_focal_learners` | `update_focal_learners_command` | |
| `POST /experiments/{experiment_id}/end` | `end_experiment` | `end_experiment_command` | |
| `POST /experiments/{experiment_id}/sandbox` | `set_experiment_sandbox` | `set_sandbox_command` | |
| `GET /experiments/research-defaults` | `get_research_defaults` | `none` | transport-only |
| `GET /experiments/{experiment_id}/story` | `get_experiment_story` | `ExperimentStoryApplicationService.build_experiment_story` | session |
| `GET /experiments/{experiment_id}` | `get_experiment` | `ExperimentViewQuery.build_detail` | |
| `GET /experiments/{experiment_id}/summary` | `get_experiment_summary` | `ExperimentViewQuery.build_view` | |
| `GET /experiments/{experiment_id}/workflow` | `get_experiment_workflow` | `ExperimentWorkflowQuery.compute` | |
| `GET /experiments/{experiment_id}/provenance` | `get_experiment_provenance` | `StudyRecordQuery.provenance` | |
| `GET /experiments/{experiment_id}/rater-schedule` | `get_rater_schedule` | `StudyRecordQuery.schedule` | |
| `GET /experiments/{experiment_id}/study-results` | `get_study_results` | `StudyRecordQuery.results` | |
| `GET /experiments/investigations/{investigation_id}/study-results` | `get_study_wide_results` | `StudyRecordQuery.study_results` | |
| `GET /experiments/{experiment_id}/transcripts` | `get_transcripts` | `StudyRecordQuery.transcripts` | |
| `GET /experiments/investigations/{investigation_id}/design` | `get_study_design` | `StudyRecordQuery.design` | |
| `POST /experiments/{experiment_id}/executions` | `create_experiment_execution` | `LaunchExecution` | |
| `POST /experiments/{experiment_id}/conditions/{condition_code}/retry` | `retry_experiment_condition` | `retry_condition` | |
| `POST /experiments/{experiment_id}/synthetic-students` | `trigger_synthetic_students` | `none` | dispatch |
| `POST /experiments/{experiment_id}/synthetic-rate` | `trigger_synthetic_rate` | `none` | dispatch |
| `POST /experiments/{experiment_id}/synthetic-teacher` | `trigger_synthetic_teacher` | `none` | dispatch |
| `POST /experiments/{experiment_id}/synthetic-loop` | `trigger_synthetic_loop` | `none` | dispatch |
| `WEBSOCKET /experiments/{experiment_id}/synthetic/ws` | `synthetic_progress_ws` | `none` | transport-only |
| `GET /experiments/executions/{execution_id}` | `get_execution` | `ExperimentExecutionViewQuery.build_detail` | |
| `POST /experiments/executions/{execution_id}/packets/export` | `export_execution_packets` | `PacketExportApplicationService.export_packets` | |
| `experiments.retry_condition_run` | `retry_failed_condition` | `retry_failed_condition` | |
| `experiments.run_conditioned_execution` | `conduct_conditioned_execution` | `conduct_conditioned_execution` | |
| `experiments.author_plan` | `draft_experiment_plan` | `ExperimentApplicationService.draft_experiment_plan` | |

## Operation shape

The ratchet recognizes a use case that has these properties:

- It takes one per-call input.
- It returns an explicit output.
- Neither type names a framework or infrastructure type.
- Its collaborators are bound at construction.

```python
class LaunchExecution:
    def __init__(self, store: ExecutionLaunchStore) -> None: ...

    async def __call__(self, request: LaunchExecutionInput) -> LaunchExecutionOutput: ...
```

`LaunchExecution` in `src/app/domains/experiments/application/execution_launch.py` is the only
recognized operation. The guard also checks these launch-path callables. None of them has the shape:

- `retry_condition`
- `create_execution`
- `retry_failed_condition`
- `conduct_conditioned_execution`
