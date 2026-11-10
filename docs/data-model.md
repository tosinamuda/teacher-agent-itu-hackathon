# Data model

The MySQL schema: 74 tables. `src/app/db/metadata.py` registers the 73 ORM models. The Casbin adapter owns `casbin_rule`. Alembic revision `0025_job_results` builds the schema. Terms: [glossary.md](glossary.md).

## 1. Conventions

- Each entity has a UUID primary key `id`, stored as `CHAR(32)`.
- Most entities also have a unique business key, such as `plan_versions.version_id` or `student_profiles.student_id`.
- Cross-table foreign keys target the business key. Every `student_id` foreign key targets `student_profiles.student_id`.

- Versioned payloads use MySQL `JSON` columns: `session_plan`, `manifest`, `payload`, `condition_profile`, `generated_pack`.
- Three ORM attributes differ from their column: `artefact_type` is `artefact_kind` on `artefacts` and `artefact_plans`. `Event.artefact_id` is `events.pack_id`.

`plan_versions.concluded_at` marks a lesson as concluded. A flush that changes a concluded lesson's rows fails with `ConcludedLessonError`, and the API returns 409.

In the trees, `─<` is one-to-many and `─>` is a foreign key.

## 2. Tables

### Users and access

| Table | Model | Key columns |
|---|---|---|
| `users` | `User` | `auth_id` (`code\|<code>`), `email`, `full_name`, `role` (`teacher`, `research_manager`, `rater`, `admin`, `student`) |
| `casbin_rule` | (adapter) | `ptype`, `v0`–`v5` |

### School

```text
School ─< Class
GradeLevel ─< Class
Subject ─< Course (courses_curriculum)
GradeLevel ─< Course
Course ─< TermClassSubject
Class ─< TermClassSubject
AcademicYear ─< Term
```

| Table | Model | Key columns |
|---|---|---|
| `schools` | `School` | `code`, `name`, `default_academic_year`, `current_term` |
| `subjects` | `Subject` | `name`, `code`, `category`, `is_trade`, `is_compulsory` |
| `grade_levels` | `GradeLevel` | `name`, `sequence` |
| `academic_years` | `AcademicYear` | `name`, `start_date`, `end_date`, `is_current` |
| `terms` | `Term` | `academic_year_id`, `name`, `is_current` |
| `classes` | `Class` | `school_id`, `grade_level_id`, `name` |
| `courses_curriculum` | `Course` | `subject_id`, `grade_level_id`, `name` |
| `term_class_subjects` | `TermClassSubject` | `course_id`, `class_id`, `term`, `year` |

### Curriculum

```text
CurriculumTheme ─< CurriculumTopic ─< CurriculumSubtopic ─< CurriculumPerformanceObjective
                                                         ─< KnowledgeComponent
                                                         ─< ClassSession
```

`curriculum_topics`, `class_sessions` and `reference_materials` name their `subject`, `track`, `grade` and `term` by foreign key to four lookup tables.

| Table | Model | Key columns |
|---|---|---|
| `curriculum_subjects`, `curriculum_tracks`, `curriculum_grades`, `curriculum_terms` | `CurriculumSubject`, `CurriculumTrack`, `CurriculumGrade`, `CurriculumTerm` | `name` |
| `curriculum_themes` | `CurriculumTheme` | `theme_key`, `title` |
| `curriculum_topics` | `CurriculumTopic` | `topic_key`, `theme_id`, `week`, `topic`, `general_objectives` |
| `curriculum_subtopics` | `CurriculumSubtopic` | `subtopic_id`, `topic_key`, `title`, `performance_objectives`, `teacher_activities`, `student_activities`, `evaluation_guide` |
| `curriculum_performance_objectives` | `CurriculumPerformanceObjective` | `curriculum_objective_id`, `subtopic_id`, `curriculum_objective_text` |
| `knowledge_components` | `KnowledgeComponent` | `kc_code`, `subtopic_id`, `description`, `bloom_level` |
| `class_sessions` | `ClassSession` | `session_id`, `topic_key`, `subtopic_id`, `week`, `duration_minutes`, `session_objectives` |
| `reference_materials` | `ReferenceMaterial` | `source_id`, `type`, `title`, `topics`, `chunk_refs` |

### Teaching

```text
TermClassSubject ─< SchemeOfWork ─< LessonPeriod ─> CurriculumSubtopic
TermClassSubject ─< TeacherWorkspace ─> User
TeacherWorkspace ─< LessonDelivery ─> (LessonPeriod, PlanVersion)
```

| Table | Model | Key columns |
|---|---|---|
| `scheme_of_work` | `SchemeOfWork` | `term_class_subject_id`, `week_number`, `title`, `objectives` |
| `lesson_periods` | `LessonPeriod` | `scheme_of_work_id`, `period_number`, `title`, `subtopic_id` |
| `teacher_workspaces` | `TeacherWorkspace` | `teacher_id` (→ `users`), `term_class_subject_id`, `is_primary`, `settings` |
| `lesson_deliveries` | `LessonDelivery` | `teacher_workspace_id`, `lesson_period_id`, `plan_version_id`, `status`, `delivered_on` |

### Learners and the class test

```text
Class ─< LearnerProfile ─> User
PlanVersion ─< ExitTicketItem ─> (CurriculumSubtopic, KnowledgeComponent)
PlanVersion ─< ExitTicketSubmission ─> LearnerProfile
ExitTicketItem ─< StudentItemResponse ─> (LearnerProfile, LessonDelivery)
```

| Table | Model | Domain | Key columns |
|---|---|---|---|
| `student_profiles` | `LearnerProfile` | learners | `student_id`, `code`, `class_id`, `user_id`, `language_level`, `pace_preference`, `time_budget_minutes` |
| `exit_ticket_items` | `ExitTicketItem` | curriculum | `plan_version_id`, `lesson_objective_id`, `stem`, `options`, `correct_option`, `option_misconceptions` |
| `exit_ticket_submissions` | `ExitTicketSubmission` | assessments | `diagnostic_id`, `student_id`, `plan_version_id`, `results`, `entered_by`, `provenance_attachment_id`, `survey_pending` |
| `student_item_responses` | `StudentItemResponse` | assessments | `item_id`, `student_id`, `lesson_delivery_id`, `choice`, `is_correct`, `score` |
| `attachments` | `Attachment` | attachments | `kind`, `content_type`, `sha256`, `stored_path`, `caption` |

`exit_ticket_submissions.results` holds the answers and the survey. The `learner_state` domain derives the per-objective learner state from it. No table stores that state. Snapshots of it live on `artefact_plans` and `experiment_focal_cases`.

### Lesson plans and content

```text
LessonPeriod ─< LessonPlan ─< PlanVersion ─< PlanVersionObjective ─> CurriculumPerformanceObjective
PlanVersion ─< ArtefactPlan ─> LearnerProfile
PlanVersion ─< Artefact ─> (LearnerProfile, ExperimentConditionRun)
Artefact ─< ContentApproval
RevisionThread ─< RevisionTurn
```

| Table | Model | Key columns |
|---|---|---|
| `lesson_plans` | `LessonPlan` | `plan_id`, `lesson_period_id`, `title`, `subject`, `grade` |
| `plan_versions` | `PlanVersion` | `version_id`, `plan_id`, `parent_version_id`, `session_plan`, `status` (`draft`, `approved`), `approved_at`, `assessment_released_at`, `concluded_at` |
| `plan_version_objectives` | `PlanVersionObjective` | `plan_version_id`, `lesson_objective_id`, `objective_order`, `curriculum_objective_id` |
| `artefact_plans` | `ArtefactPlan` | `artefact_plan_id`, `artefact_kind`, `scope`, `plan_version_id`, `student_id`, `experiment_condition_run_id`, `payload`, `learner_state_snapshot`, `status` |
| `artefacts` | `Artefact` | `artefact_id`, `artefact_kind`, `scope`, `plan_version_id`, `student_id`, `experiment_condition_run_id`, `parent_artefact_id`, `manifest`, `version`, `review_status` |
| `content_approvals` | `ContentApproval` | `approval_id`, `artefact_id`, `approved_version`, `approved_by` |
| `content_specifications` | `ContentSpecificationRecord` | `kind`, `revision`, `material`, `audience`, `structure`, `requirements` |
| `student_pack_generations` | `StudentPackGeneration` | `generation_id`, `student_id`, `plan_version_id`, `attempt_number`, `status`, `produced_artefact_id` |
| `revision_threads` | `RevisionThread` | `revision_thread_id`, `artefact_type`, `subject_id` |
| `revision_turns` | `RevisionTurn` | `thread_db_id`, `turn_number`, `instruction`, `base_version_id`, `result_version_id` |
| `figures` | `Figure` | `figure_id` (SHA-256 of the TikZ source), `source`, `svg`, `state` |

`artefact_kind` values: `lesson_plan`, `lesson_note`, `post_class_review_pack` (revision note), `diagnostic` (class test). `scope` values: `class_level`, `learner_level`. `review_status` values: `pending`, `approved`, `rejected`.

### Expert content

```text
TextbookPacket ─< TextbookRecord ─< TextbookRecordSubtopic ─> CurriculumSubtopic
AoTextbookLinkage (one per subtopic) ─< AoTextbookObjectiveLink ─< AoTextbookRecordLink ─> TextbookRecord
```

| Table | Model | Key columns |
|---|---|---|
| `textbook_packets` | `TextbookPacket` | `packet_id`, `record_count` |
| `textbook_records` | `TextbookRecord` | `record_id`, `packet_id`, `record_type`, `heading_path`, `content_text`, `retrieval_text`, `asset_refs`, `primary_subtopic_id`, `link_status` |
| `textbook_record_subtopics` | `TextbookRecordSubtopic` | `record_id`, `subtopic_id`, `is_primary` |
| `ao_textbook_linkages` | `AoTextbookLinkage` | `subtopic_id`, `status`, `shared_foundation_record_ids` |
| `ao_textbook_objective_links` | `AoTextbookObjectiveLink` | `subtopic_id`, `ao_id`, `curriculum_objective_id`, `step_blueprint`, `practice_record_ids`, `assessment` |
| `ao_textbook_record_links` | `AoTextbookRecordLink` | `subtopic_id`, `ao_id`, `record_id`, `role`, `method`, `rationale` |
| `textbook_seed_runs`, `ao_textbook_linkage_seed_runs` | `TextbookSeedRun`, `AoTextbookLinkageSeedRun` | counts and status of each seed run |

### Experiments

```text
Investigation ─< Experiment ─> (TeacherWorkspace, LessonPeriod, PlanVersion)
Experiment ─< ExperimentExecution ─< ExperimentFocalCase ─> LearnerProfile
ExperimentExecution ─< ExperimentConditionRun ─> (ExperimentFocalCase, ArtefactPlan)
Experiment ─< C4GovernanceDecision ─> ExperimentConditionRun
```

| Table | Model | Key columns |
|---|---|---|
| `investigations` | `Investigation` | `investigation_id`, `investigation_code`, `title`, `status` |
| `experiments` | `Experiment` | `experiment_id`, `experiment_code`, `investigation_db_id`, `teacher_workspace_id`, `lesson_period_id`, `plan_version_id`, `focal_learner_ids`, `lifecycle_status`, `is_sandbox` |
| `experiment_executions` | `ExperimentExecution` | `execution_id`, `experiment_db_id`, `hypothesis`, `attempt_number`, `status`, `delivery_count`, `runtime_snapshot`, `error_category` |
| `experiment_focal_cases` | `ExperimentFocalCase` | `experiment_focal_case_id`, `execution_db_id`, `student_id`, `focal_case_type`, `learner_state_snapshot` |
| `experiment_condition_runs` | `ExperimentConditionRun` | `experiment_condition_run_id`, `execution_db_id`, `focal_case_db_id`, `hypothesis`, `condition_code`, `artefact_plan_id`, `status`, `condition_profile`, `validation_result`, `generated_pack`, `model_name`, `prompt_version` |
| `c4_governance_decisions` | `C4GovernanceDecision` | `decision_id`, `experiment_db_id`, `experiment_condition_run_id`, `teacher_decision`, `regeneration_count`, `issue_category`, `review_time_seconds` |

`focal_case_type` values: `remediate`, `reinforce`, `extend`, `mixed_or_misconception`.

No code writes `c4_governance_decisions`. The teacher's C4 decision is the `review_status` of the C4 artefact.

### Evaluation

```text
User ─< EvaluationRater ─< RaterAssignment ─> Experiment
ExperimentExecution ─< EvaluationPacket ─> ExperimentConditionRun (primary)
EvaluationPacket ─< EvaluationRating ─> EvaluationRater
ExperimentExecution ─< EvaluationAuditItem ─< EvaluationAuditRating ─> EvaluationRater
```

| Table | Model | Key columns |
|---|---|---|
| `evaluation_raters` | `EvaluationRater` | `rater_id`, `display_name`, `user_id`, `origin` |
| `rater_assignments` | `RaterAssignment` | `assignment_id`, `experiment_db_id`, `rater_db_id`, `hypothesis`, `scope_id`, `is_adjudicator` |
| `evaluation_packets` | `EvaluationPacket` | `evaluation_packet_id`, `packet_code`, `execution_db_id`, `hypothesis`, `primary_condition_run_id`, `condition_run_ids`, `export_refs` |
| `evaluation_ratings` | `EvaluationRating` | `rating_id`, `evaluation_packet_db_id`, `rater_db_id`, `rubric_scores`, `section_scores`, `overall_score` |
| `evaluation_audit_items` | `EvaluationAuditItem` | `audit_item_id`, `execution_db_id`, `condition_code`, `lesson_objective_id`, `generated_excerpt`, `source_ref`, `source_excerpt`, `scope_boundary` |
| `evaluation_audit_ratings` | `EvaluationAuditRating` | `audit_item_db_id`, `rater_db_id`, `source_relevance`, `support_sufficiency`, `faithfulness`, `scope_correctness` (0–2 each), `source_grounding_score` |

### Study record

The MSc field study, imported from its published release. Once a lesson concludes, the concluded-lesson guard refuses changes to its rows.

| Table | Model | Key columns |
|---|---|---|
| `study_imports` | `StudyImport` | `investigation_id`, `release`, `importer` |
| `study_transcripts` | `StudyTranscript` | `plan_version_id`, `kind`, `student_id`, `pages`, `body`, `sha256` |
| `study_classwork_questions` | `StudyClassworkQuestion` | `plan_version_id`, `question_n`, `lesson_objective_id`, `text`, `answer` |
| `study_classwork_scripts` | `StudyClassworkScript` | `plan_version_id`, `student_id`, `teacher_total` |
| `study_classwork_answers` | `StudyClassworkAnswer` | `script_id`, `question_n`, `mark`, `working`, `misconception_code` |
| `study_criterion_scores` | `StudyCriterionScore` | `artefact_id`, `rater_db_id`, `lesson_objective_id`, `criterion_id`, `score` (1–5) |
| `study_comparative_judgements` | `StudyComparativeJudgement` | `artefact_a_id`, `artefact_b_id`, `rater_db_id`, `criterion_id`, `choice`, `favoured_condition` |
| `study_rating_documents` | `StudyRatingDocument` | `document`, `rater_db_id`, `part`, `artefact_a_id`, `artefact_b_id`, `state`, `closing_comment` |

### Infrastructure

| Table | Model | Key columns |
|---|---|---|
| `jobs` | `Job` | `job_id`, `kind`, `args`, `subject`, `active_subject`, `state`, `attempts`, `runner`, `lease_expires_at`, `result`, `requested_by` |
| `job_runners` | `JobRunner` | `runner`, `slots`, `running`, `seen_at` |
| `progress_events` | `ProgressEvent` | `id` (auto-increment), `channel`, `payload` |
| `generation_events` | `GenerationEvent` | `seq`, `id`, `kind`, `model`, `correlation_id`, `request`, `response`, `token_usage` |
| `events` | `Event` | `event_id`, `student_id`, `pack_id`, `event_type`, `payload` |

<a id="3-reproducibility-snapshot-why-the-_json-columns-exist"></a>

## 3. Reproducibility snapshot

These columns record the inputs of each generation.

| Table | Columns |
|---|---|
| `experiment_condition_runs` | `condition_profile`, `validation_result`, `generated_pack`, `model_name`, `prompt_version` |
| `experiment_executions` | `runtime_snapshot` |
| `experiment_focal_cases`, `artefact_plans` | `learner_state_snapshot`: the learner state that P1 used |
| `generation_events` | one row per LLM call, with the request and the response |

## 4. Dual-key identifier pattern

`scripts/seed_jss1_curriculum.py` builds the curriculum keys from `dataset/processed/`.

| Entity | Business key | Example |
|---|---|---|
| `CurriculumTopic` | `topic_key` | `jss1-math-addition-and-subtraction` |
| `CurriculumSubtopic` | `subtopic_id` | `jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values` |
| `CurriculumPerformanceObjective` | `curriculum_objective_id` | `<subtopic_id>-po01` |
| `ClassSession` | `session_id` | `session-<subtopic_id>` |
| `KnowledgeComponent` | `kc_code` | `JSS1-GMATH-3DF-001` |
| Lesson-plan objective | `lesson_objective_id` | `lop01` |

`session_plan` payloads, API URLs, seed scripts and logs use the business key.
