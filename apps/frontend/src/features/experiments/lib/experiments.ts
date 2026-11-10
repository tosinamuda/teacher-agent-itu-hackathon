import { ContentBlock, LessonStepStructured } from "@/shared/types/lesson-schema";

/** Supported experiment hypotheses. */
export const EXPERIMENT_HYPOTHESES = ["H1", "H2"] as const;

/**
 * Supported condition codes across H1 and H2 — the single frontend source of truth.
 * H1 conditions are the `C*` codes; H2 conditions are the `P*` codes. Adding/removing a
 * condition is a one-line edit here (everything that lists conditions derives from this).
 */
export const CONDITION_CODES = ["C0", "C1", "C2", "C3", "C4", "P0", "P1"] as const;

/** Known execution status values. */
export const EXECUTION_STATUSES = [
  "draft",
  "queued",
  "running",
  "succeeded",
  "failed",
  "cancelled",
] as const;

/** Hypothesis identifier. */
export type Hypothesis = (typeof EXPERIMENT_HYPOTHESES)[number];

/** Condition identifier. */
export type ConditionCode = (typeof CONDITION_CODES)[number];

/** Execution state identifier. */
export type ExecutionStatus = (typeof EXECUTION_STATUSES)[number];

/** Packet export state. */
export type PacketStatus = "draft" | "queued" | "exported" | "failed" | "ready";

/** Persisted focal-case category. */
export type FocalCaseType =
  | "remediate"
  | "reinforce"
  | "extend"
  | "mixed_or_misconception";

/** Human-facing readiness flags for an experiment. */
export type ExperimentReadiness = {
  lesson_approved: boolean;
  baseline_selected: boolean;
  h1_ready: boolean;
  base_pack_ready: boolean;
  base_pack_approved?: boolean;
  /** The class base-pack artefact the teacher reviews + accepts (null before it
   *  has been generated). The teacher's review page links to this id. */
  base_pack_artefact_id?: string | null;
  /** H2's base: the first draw's C3 pack, approved programmatically in C4's place. */
  h2_base_pack_artefact_id?: string | null;
  h2_base_approved?: boolean;
  /** The lesson's newest lesson note, and whether the teacher has approved it. The
   *  class revision note is grounded in it, so it waits for the approval. */
  lesson_note_artefact_id?: string | null;
  lesson_note_approved?: boolean;
  learner_evidence_ready: boolean;
  h2_ready: boolean;
};

/** One live progress event streamed over the synthetic-test WebSocket. */
export type SyntheticProgressEvent = {
  type: "start" | "progress" | "done" | "error";
  flow: string;
  phase: string;
  done?: number;
  total?: number;
  message?: string;
};

/** Hypothesis-specific experiment summary used by split H1/H2 pages. */
export type ExperimentHypothesisSummary = {
  ready: boolean;
  execution_count: number;
  latest_execution_id?: string | null;
  latest_execution_status?: string | null;
  latest_attempt_number?: number | null;
};

/** Filter values used by the experiment list page. */
export type ExperimentFilters = {
  schoolId?: string;
  teacherId?: string;
  teacherWorkspaceId?: string;
  experimentCode?: string;
  query?: string;
  hypothesis?: Hypothesis | "";
  status?: string;
};

/** Payload used when creating an experiment container. */
export type ExperimentCreateRequest = {
  /** The parent study — every experiment belongs to one. */
  investigation_id: string;
  teacher_workspace_id: string;
  /** The experiment is created against a lesson; its own plan is authored after. */
  lesson_period_id: string;
};

/** Selector option for researcher-facing workspace picking. */
export type ExperimentWorkspaceOption = {
  teacher_workspace_id: string;
  term_class_subject_id: string;
  school_id: string;
  school_name: string;
  school_code: string;
  class_id: string;
  class_name: string;
  subject_name: string;
  subject_code: string;
  grade_level: string;
  term: string;
  academic_year: string;
  teacher_id: string;
  teacher_name?: string | null;
  workspace_name: string;
  is_primary: boolean;
};

/** Selector option for lesson picking inside a workspace. */
export type ExperimentLessonOption = {
  lesson_period_id: string;
  week_number: number;
  period_number: number;
  lesson_title: string;
  lesson_subtitle?: string | null;
  approved_version_count: number;
  latest_approved_version_id?: string | null;
  latest_approved_version_label?: string | null;
};

/** Selector option for approved baseline version picking. */
export type ExperimentApprovedVersion = {
  plan_id: string;
  plan_version_id: string;
  lesson_period_id?: string | null;
  lesson_title: string;
  lesson_subtitle?: string | null;
  version_label: string;
  approved_at?: string | null;
  approved_by?: string | null;
};

/** Candidate learner that can be saved for H2. */
export type ExperimentFocalLearnerOption = {
  learner_id: string;
  learner_name: string;
  latest_diagnostic_id?: string | null;
  has_evidence: boolean;
  latest_submitted_at?: string | null;
};

/** Summary row shown in the experiments list. */
/** Configured default lesson context for the synthetic harness (a 3rd-term subtopic). */
export type ResearchDefaults = {
  grade: string;
  subject: string;
  term: string;
  subtopic: string;
};

export type ExperimentSummary = {
  experiment_id: string;
  experiment_code: string;
  teacher_workspace_id: string;
  workspace_name?: string | null;
  teacher_id?: string | null;
  teacher_name?: string | null;
  school_id?: string | null;
  school_name?: string | null;
  school_code?: string | null;
  class_id?: string | null;
  class_name?: string | null;
  subject_name?: string | null;
  subject_code?: string | null;
  grade_level?: string | null;
  term?: string | null;
  academic_year?: string | null;
  // Null while the experiment awaits its own teacher-authored plan.
  plan_version_id: string | null;
  baseline_version_label?: string | null;
  baseline_approved_by?: string | null;
  lesson_period_id?: string | null;
  lesson_title?: string | null;
  lesson_subtitle?: string | null;
  learner_count: number;
  diagnostic_count: number;
  focal_learner_count: number;
  readiness: ExperimentReadiness;
  h1_summary: ExperimentHypothesisSummary;
  h2_summary: ExperimentHypothesisSummary;
  hypothesis?: Hypothesis | null;
  status: string;
  lifecycle_status?: string;
  ended_at?: string | null;
  ended_by?: string | null;
  is_sandbox?: boolean;
  execution_count?: number | null;
  latest_execution_status?: string | null;
  created_at?: string | null;
  /** Derived from ratings: synthetic, live, mixed, or null (not yet evaluated). */
  evaluation_mode?: "synthetic" | "live" | "mixed" | null;
  /** Parent study (containment breadcrumb); null when the lesson is in no investigation. */
  investigation_id?: string | null;
  investigation_code?: string | null;
};

/** Per-hypothesis rater-rating progress for a study. */
export type RatingsHypothesisSummary = {
  packet_count: number;
  rating_count: number;
  mean_overall: number | null;
};

/** Synthetic dry-run (proxy) ratings — excluded from the reported expert numbers. */
export type SyntheticRatingsSummary = {
  rating_count: number;
  rated_packet_count: number;
  distinct_raters: number;
  mean_overall: number | null;
  /** Mean overall per condition code (C0–C4 / P0–P1). */
  by_condition: Record<string, number | null>;
};

/**
 * Rater-rating progress for a study (research results dashboard). Top-level fields are
 * expert-only (the reported numbers); `synthetic` carries the dry-run proxy separately.
 */
export type ExperimentRatingsSummary = {
  experiment_id: string;
  packet_count: number;
  rated_packet_count: number;
  total_ratings: number;
  distinct_raters: number;
  mean_overall: number | null;
  by_hypothesis: Record<string, RatingsHypothesisSummary>;
  synthetic: SyntheticRatingsSummary | null;
};

/** One member experiment of a study, projected for the study dashboard. */
export type InvestigationExperimentRow = {
  experiment_id: string;
  experiment_code: string;
  lesson_period_id?: string | null;
  lesson_title?: string | null;
  lesson_subtitle?: string | null;
  week_number?: number | null;
  period_number?: number | null;
  school_name?: string | null;
  class_name?: string | null;
  subject_name?: string | null;
  grade_level?: string | null;
  term?: string | null;
  plan_version_id?: string | null;
  status: string;
  lifecycle_status?: string;
  is_sandbox?: boolean;
};

/** An investigation (study) row in the list — the explicit parent of its experiments. */
export type InvestigationSummary = {
  investigation_id: string;
  investigation_code: string;
  title: string;
  description?: string | null;
  status: string;
  experiment_count: number;
  ended_at?: string | null;
  ended_by?: string | null;
  created_at?: string | null;
};

/** Full investigation detail: its member experiments. */
export type InvestigationDetail = InvestigationSummary & {
  experiments: InvestigationExperimentRow[];
};

/** Create-investigation payload (the study is created empty; experiments are added after). */
export type InvestigationCreateRequest = {
  title: string;
  description?: string | null;
};

/** One experiment's rating result within an investigation rollup. */
export type InvestigationExperimentResult = {
  experiment_id: string;
  packet_count: number;
  rated_packet_count: number;
  total_ratings: number;
  mean_overall: number | null;
};

/** Rolled-up rater results across all experiments in an investigation's scope. */
export type InvestigationResultsRollup = {
  investigation_id: string;
  experiment_count: number;
  packet_count: number;
  rated_packet_count: number;
  total_ratings: number;
  distinct_raters: number;
  mean_overall: number | null;
  per_experiment: InvestigationExperimentResult[];
};

/** One row of an offline (bulk) rating import. */
export type RatingImportRow = {
  packet_code: string;
  rater_name: string;
  overall_score: number;
  rubric_scores?: Record<string, number>;
  notes?: string;
};

/** The outcome of an offline rating import. */
export type RatingImportResult = {
  imported: number;
  updated: number;
  skipped: number;
  errors: string[];
};

/** A study-pack section rendered in the comparison/presentation views. */
export type ComparePackStep = {
  step_id: string;
  title?: string | null;
  lesson_objective_id?: string | null;
  personalisation_band?: string | null;
  blocks: ContentBlock[];
};

/** A study-pack manifest, rendered side by side in the comparison view. */
export type ComparePackManifest = {
  artefact_id: string;
  subject?: string | null;
  grade?: string | null;
  topic?: string | null;
  subtopic?: string | null;
  steps: ComparePackStep[];
};

/** One H1 condition (C0–C4) and its rendered base pack. */
export type CompareConditionPack = {
  condition_code: string;
  artefact_id: string | null;
  manifest: ComparePackManifest | null;
};

/** One band's H2 packs: the shared base (P0) vs the personalised pack (P1). */
export type CompareBandPack = {
  band: string;
  learner_id: string;
  base: ComparePackManifest | null;
  personalised: ComparePackManifest | null;
};

/** The full condition comparison for one experiment/lesson. */
export type ExperimentComparison = {
  experiment_id: string;
  h1: CompareConditionPack[];
  h2_bands: CompareBandPack[];
};

/** One MCQ item shown in the journey diagnostic step (no answers exposed). */
export type DiagnosticQuestionItem = {
  item_id: string;
  stem: string;
  options: Record<string, string>;
  difficulty?: string | null;
};

/** A lesson objective with its MCQ items (the diagnostic the student took). */
export type DiagnosticObjectiveQuestions = {
  lesson_objective_id: string;
  objective_text?: string | null;
  items: DiagnosticQuestionItem[];
};

/** The lesson's per-objective MCQ diagnostic for the journey view. */
export type DiagnosticQuestions = {
  plan_version_id: string;
  subject?: string | null;
  topic?: string | null;
  subtopic?: string | null;
  objectives: DiagnosticObjectiveQuestions[];
};

/** Execution launch payload. */
export type ExperimentExecutionCreateRequest = {
  hypothesis: Hypothesis;
  runtime_snapshot?: Record<string, unknown>;
};

/** Experiment condition run detail. */
export type ExperimentConditionRun = {
  condition_run_id: string;
  execution_id: string;
  condition_code: ConditionCode;
  hypothesis: Hypothesis;
  status: string;
  artefact_plan_id?: string | null;
  artefact_build_job_id?: string | null;
  artefact_id?: string | null;
  learner_id?: string | null;
  focal_case_id?: string | null;
  error_message?: string | null;
};

/** Experiment focal-case detail. */
export type ExperimentFocalCase = {
  focal_case_id: string;
  execution_id: string;
  learner_id: string;
  learner_name?: string | null;
  focal_type: FocalCaseType;
  learner_state_snapshot?: Record<string, unknown> | null;
  selection_metadata?: Record<string, unknown> | null;
};

/** Exported evaluation packet detail. */
export type EvaluationPacket = {
  packet_id: string;
  packet_code: string;
  execution_id: string;
  hypothesis: Hypothesis;
  status: PacketStatus | string;
  primary_condition_run_id: string;
  experiment_focal_case_id?: string | null;
  condition_run_ids?: string[] | null;
  export_refs?: Record<string, unknown> | null;
  artefact_ids?: string[] | null;
};

/** Structured failure category set by the backend worker (null unless failed). */
export type ExecutionErrorCategory =
  | "inputs_missing"
  | "persistence"
  | "generation"
  | "cancelled";

/** Execution detail shown in the experiment page. */
export type ExperimentExecution = {
  execution_id: string;
  experiment_id: string;
  hypothesis: Hypothesis;
  attempt_number: number;
  status: ExecutionStatus | string;
  created_at?: string | null;
  updated_at?: string | null;
  error_message?: string | null;
  /** Why it failed, classified server-side by exception type. */
  error_category?: ExecutionErrorCategory | string | null;
  runtime_snapshot?: Record<string, unknown> | null;
  condition_runs?: ExperimentConditionRun[];
  focal_cases?: ExperimentFocalCase[];
  packets?: EvaluationPacket[];
};

/** Full experiment detail contract. */
export type ExperimentDetail = ExperimentSummary & {
  executions?: ExperimentExecution[];
  focal_learner_candidates?: ExperimentFocalLearnerOption[];
  selected_focal_learners?: ExperimentFocalLearnerOption[];
};

/** Packet export response contract. */
export type ExperimentPacketExportResponse = {
  execution_id: string;
  hypothesis: Hypothesis;
  packet_count: number;
  packets: EvaluationPacket[];
};

/** Builds the query string for the experiment list API. */
export const buildExperimentQuery = (filters: ExperimentFilters) => {
  const params = new URLSearchParams();
  if (filters.schoolId) params.set("school_id", filters.schoolId);
  if (filters.teacherId) params.set("teacher_id", filters.teacherId);
  if (filters.teacherWorkspaceId) {
    params.set("teacher_workspace_id", filters.teacherWorkspaceId);
  }
  if (filters.experimentCode) params.set("experiment_code", filters.experimentCode);
  if (filters.query) params.set("query", filters.query);
  if (filters.hypothesis) params.set("hypothesis", filters.hypothesis);
  if (filters.status) params.set("status", filters.status);
  return params.toString();
};

/** Returns the primary human-facing experiment title. */
export const experimentTitle = (experiment: ExperimentSummary | null) =>
  experiment?.lesson_title?.trim() ||
  experiment?.lesson_subtitle?.trim() ||
  experiment?.experiment_code ||
  "Experiment";

/** Returns the human-facing subtitle shown under experiment titles. */
export const experimentSubtitle = (experiment: ExperimentSummary | null) => {
  const parts = [
    experiment?.school_name,
    experiment?.class_name,
    experiment?.subject_name,
    experiment?.teacher_name,
  ]
    .map((part) => part?.trim())
    .filter((part): part is string => Boolean(part));
  return parts.join(" • ");
};

/** Returns the tone token used for status pills. */
export const executionStatusTone = (status: string) => {
  const value = status.toLowerCase();
  if (value.includes("fail")) return "danger";
  if (value.includes("run")) return "warning";
  if (value.includes("succeed") || value.includes("complete")) return "success";
  return "muted";
};

/** Returns the expected condition set for a hypothesis, derived from CONDITION_CODES. */
export const conditionCodesForHypothesis = (hypothesis: Hypothesis): ConditionCode[] =>
  CONDITION_CODES.filter((code) =>
    hypothesis === "H1" ? code.startsWith("C") : code.startsWith("P"),
  );

/** One pipeline step of an experiment, with its generation-log trace (if any). */
export type ExperimentStoryStage = {
  key: string;
  title: string;
  llm: boolean;
  correlation_ids: string[];
  event_count: number;
  note: string | null;
};

/** The scheme-of-work context a lesson sits in (the teacher's starting point). */
export type ExperimentStoryCurriculum = {
  subject?: string | null;
  grade?: string | null;
  term?: string | null;
  week?: string | number | null;
  topic?: string | null;
  subtopic?: string | null;
};

/** The teacher's authored lesson plan (subset rendered in the story opener). */
export type ExperimentStoryLessonPlan = {
  theme?: string | null;
  curriculum_objectives?: { objective_text?: string }[];
  lesson_plan_objectives?: {
    lesson_objective_id?: string;
    objective_text?: string;
    kc_type?: string | null;
  }[];
  entry_behaviour?: string[];
  instructional_materials?: string[];
  references?: string[];
  steps?: LessonStepStructured[];
};

/** An experiment's pipeline as an ordered, log-traceable story. */
export type ExperimentStory = {
  experiment_id: string;
  plan_version_id: string;
  lesson_title: string | null;
  curriculum?: ExperimentStoryCurriculum | null;
  lesson_plan?: ExperimentStoryLessonPlan | null;
  stages: ExperimentStoryStage[];
};

/** Summary stats for one condition group (n / mean / sample SD). */
export type GroupStat = { n: number; mean: number | null; std: number | null; ci?: number };

/** A two-group contrast: mean difference + significance + effect sizes. */
export type StatContrast = {
  mean_diff: number;
  mann_whitney_p: number | null;
  cliffs_delta: number | null;
  cohens_d: number | null;
};

/** An adjacent-condition contrast (e.g. C2 vs C1) for the pairwise effect plot. */
export type ContrastRow = StatContrast & { from: string; to: string };

/** Pass/partial/fail counts per source-grounding criterion + mean composite. */
export type SourceAuditDescriptives = {
  n_items: number;
  n_ratings: number;
  mean_score: number | null;
  criteria: Record<string, { fail: number; partial: number; pass: number }>;
};

/** One lesson/focal-learner P0->P1 paired score for the H2 paired plot. */
export type H2Pair = { label: string; p0: number | null; p1: number | null };

/**
 * Within-rating paired P0 (base/class) vs P1 (candidate/personalised) comparison —
 * each rating scored both packs for the same focal learner, so the contrast is
 * paired (Wilcoxon signed-rank). `by_focal` holds per-focal-learner paired means.
 */
export type H2PairedComparison = {
  n_pairs: number;
  p0: GroupStat;
  p1: GroupStat;
  mean_diff: number | null;
  wilcoxon_p: number | null;
  cliffs_delta: number | null;
  by_focal: H2Pair[];
};

/** H1/H2 hypothesis tests + chart aggregations over an experiment's ratings. */
export type ExperimentStatistics = {
  experiment_id: string;
  /** True when the figures are computed from synthetic dry-run ratings (no expert data yet). */
  synthetic?: boolean;
  h1: {
    conditions: Record<string, GroupStat>;
    dimensions: Record<string, Record<string, number | null>>;
    contrasts: ContrastRow[];
    kruskal_p: number | null;
    c0_vs_strongest: StatContrast | null;
    n_ratings: number;
  };
  h2: {
    conditions: Record<string, GroupStat>;
    pairs: H2Pair[];
    p1_vs_p0: StatContrast | null;
    /** Within-rating paired base-vs-personalised contrast (the personalisation test). */
    paired_p0_p1: H2PairedComparison;
    n_ratings: number;
  };
  source_audit: SourceAuditDescriptives;
  inter_rater: { krippendorff_alpha: number | null; n_raters: number; n_items: number };
  notes: string[];
};
