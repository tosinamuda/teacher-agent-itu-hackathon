import type { JobAccepted } from "@/shared/api/jobs";
import { API_BASE_URL, apiFetch, apiFetchBlob } from "@/shared/api/client";
import { approveContent, findContent } from "@/features/content/api/content";
import type { ContentItem } from "@/features/content/types";

import {
  ExperimentApprovedVersion,
  ExperimentConditionRun,
  ExperimentCreateRequest,
  ExperimentDetail,
  ExperimentExecution,
  ExperimentExecutionCreateRequest,
  ExperimentFocalCase,
  ExperimentFocalLearnerOption,
  ExperimentFilters,
  ExperimentLessonOption,
  ExperimentPacketExportResponse,
  ExperimentRatingsSummary,
  ExperimentStatistics,
  ExperimentStory,
  ExperimentSummary,
  ExperimentWorkspaceOption,
  EvaluationPacket,
  ComparePackManifest,
  DiagnosticQuestions,
  InvestigationCreateRequest,
  InvestigationDetail,
  InvestigationResultsRollup,
  InvestigationSummary,
  RatingImportResult,
  RatingImportRow,
  ResearchDefaults,
  buildExperimentQuery,
} from "./experiments";

type ExperimentConditionRunPayload = {
  experiment_condition_run_id: string;
  hypothesis: ExperimentConditionRun["hypothesis"];
  condition_code: ExperimentConditionRun["condition_code"];
  learner_id?: string | null;
  artefact_plan_id?: string | null;
  artefact_build_job_id?: string | null;
  artefact_id?: string | null;
  status: string;
  error_message?: string | null;
};

type ExperimentFocalCasePayload = {
  experiment_focal_case_id: string;
  learner_id: string;
  focal_case_type: ExperimentFocalCase["focal_type"];
  learner_state_snapshot?: Record<string, unknown> | null;
  selection_metadata?: Record<string, unknown> | null;
};

type EvaluationPacketPayload = {
  evaluation_packet_id: string;
  packet_code: string;
  hypothesis: ExperimentConditionRun["hypothesis"];
  status: string;
  primary_condition_run_id: string;
  experiment_focal_case_id?: string | null;
  export_refs?: Record<string, unknown> | null;
  condition_run_ids?: string[];
};

type ExperimentExecutionPayload = Omit<
  ExperimentExecution,
  "condition_runs" | "focal_cases" | "packets"
> & {
  condition_runs?: ExperimentConditionRunPayload[];
  focal_cases?: ExperimentFocalCasePayload[];
  packets?: EvaluationPacketPayload[];
};

type ExperimentDetailPayload = {
  experiment: ExperimentSummary;
  executions?: ExperimentExecutionPayload[];
  focal_learner_candidates?: ExperimentFocalLearnerOption[];
  selected_focal_learners?: ExperimentFocalLearnerOption[];
};

type ExperimentFocalLearnerSelectionPayload = {
  experiment_id: string;
  learner_ids: string[];
  candidates?: ExperimentFocalLearnerOption[];
};

type ExperimentPacketExportPayload = {
  execution_id: string;
  hypothesis: ExperimentExecution["hypothesis"];
  packet_count: number;
  packets?: EvaluationPacketPayload[];
};

const normalizeConditionRun = (
  executionId: string,
  run: ExperimentConditionRunPayload
): ExperimentConditionRun => ({
  condition_run_id: run.experiment_condition_run_id,
  execution_id: executionId,
  condition_code: run.condition_code,
  hypothesis: run.hypothesis,
  status: run.status,
  artefact_plan_id: run.artefact_plan_id ?? null,
  artefact_build_job_id: run.artefact_build_job_id ?? null,
  artefact_id: run.artefact_id ?? null,
  learner_id: run.learner_id ?? null,
  focal_case_id: null,
  error_message: run.error_message ?? null,
});

const normalizeFocalCase = (
  executionId: string,
  focalCase: ExperimentFocalCasePayload
): ExperimentFocalCase => ({
  focal_case_id: focalCase.experiment_focal_case_id,
  execution_id: executionId,
  learner_id: focalCase.learner_id,
  focal_type: focalCase.focal_case_type,
  learner_state_snapshot: focalCase.learner_state_snapshot ?? null,
  selection_metadata: focalCase.selection_metadata ?? null,
});

const normalizePacket = (
  executionId: string,
  packet: EvaluationPacketPayload
): EvaluationPacket => ({
  packet_id: packet.evaluation_packet_id,
  packet_code: packet.packet_code,
  execution_id: executionId,
  hypothesis: packet.hypothesis,
  status: packet.status,
  primary_condition_run_id: packet.primary_condition_run_id,
  experiment_focal_case_id: packet.experiment_focal_case_id ?? null,
  condition_run_ids: packet.condition_run_ids ?? [],
  export_refs: packet.export_refs ?? null,
  artefact_ids: null,
});

const normalizeExecution = (
  execution: ExperimentExecutionPayload
): ExperimentExecution => ({
  ...execution,
  condition_runs: (execution.condition_runs ?? []).map((run) =>
    normalizeConditionRun(execution.execution_id, run)
  ),
  focal_cases: (execution.focal_cases ?? []).map((focalCase) =>
    normalizeFocalCase(execution.execution_id, focalCase)
  ),
  packets: (execution.packets ?? []).map((packet) =>
    normalizePacket(execution.execution_id, packet)
  ),
});

/** Lists experiments using the active filter state. */
export const listExperiments = async (filters: ExperimentFilters) => {
  const query = buildExperimentQuery(filters);
  return apiFetch<ExperimentSummary[]>(`/experiments${query ? `?${query}` : ""}`);
};

/** Creates a new lesson-scoped experiment container (researcher; no plan yet). */
export const createExperiment = async (payload: ExperimentCreateRequest) =>
  apiFetch<ExperimentSummary>("/experiments", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** The job kind that drafts an experiment's own plan, as the server names it. */
export const AUTHOR_EXPERIMENT_PLAN = "experiments.author_plan";

/** The job kind that runs one execution (H1's build of the class note, or H2); its subject is the execution. */
export const RUN_CONDITIONED_EXECUTION = "experiments.run_conditioned_execution";

/**
 * Queue the experiment's OWN plan draft (the assigned teacher; mints a fresh plan). Answers
 * with the job drafting it, or the one already drafting it; its subject is the experiment.
 */
export const authorExperimentPlan = async (experimentId: string) =>
  apiFetch<JobAccepted>(`/experiments/${encodeURIComponent(experimentId)}/plan`, {
    method: "POST",
  });

/** Freeze the experiment's plan (the teacher's acceptance) — triggers generation.
 *  ``acceptedVersionId`` re-binds to a revised head version from the feedback loop. */
export const freezeExperimentPlan = async (
  experimentId: string,
  acceptedVersionId?: string | null
) =>
  apiFetch<ExperimentSummary>(`/experiments/${encodeURIComponent(experimentId)}/plan/freeze`, {
    method: "POST",
    body: JSON.stringify(
      acceptedVersionId ? { accepted_version_id: acceptedVersionId } : {}
    ),
  });

/** Fetches a single experiment detail payload. */
export const getExperiment = async (experimentId: string) => {
  const response = await apiFetch<ExperimentDetailPayload>(`/experiments/${experimentId}`);
  return {
    ...response.experiment,
    executions: (response.executions ?? []).map(normalizeExecution),
    focal_learner_candidates: response.focal_learner_candidates ?? [],
    selected_focal_learners: response.selected_focal_learners ?? [],
  } satisfies ExperimentDetail;
};

/**
 * Fetches one experiment's header only — the teacher-accessible read.
 *
 * The teacher role holds no ``experiment:* read`` verb (experiment detail is a
 * researcher surface), so the teacher lesson-prep + plan-review pages use this
 * header endpoint instead of {@link getExperiment}. It is guarded by the same
 * ``lesson_plan:* author_plan`` gate as the experiments list and carries none of
 * the researcher-only detail (executions / focal candidates / result summary).
 */
export const getExperimentSummary = async (experimentId: string) =>
  apiFetch<ExperimentSummary>(`/experiments/${encodeURIComponent(experimentId)}/summary`);

/** Launches an experiment execution. */
export const launchExperimentExecution = async (
  experimentId: string,
  payload: ExperimentExecutionCreateRequest
) =>
  apiFetch<ExperimentExecution>(`/experiments/${experimentId}/executions`, {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** Fetches a single execution detail payload. */
export const getExperimentExecution = async (executionId: string) => {
  const response = await apiFetch<ExperimentExecutionPayload>(
    `/experiments/executions/${executionId}`
  );
  return normalizeExecution(response);
};

/** Exports evaluation packets for an execution. */
export const exportExperimentPackets = async (
  executionId: string
): Promise<ExperimentPacketExportResponse> => {
  const response = await apiFetch<ExperimentPacketExportPayload>(
    `/experiments/executions/${executionId}/packets/export`,
    { method: "POST" }
  );
  return {
    execution_id: response.execution_id,
    hypothesis: response.hypothesis,
    packet_count: response.packet_count,
    packets: (response.packets ?? []).map((packet) =>
      normalizePacket(response.execution_id, packet)
    ),
  };
};

/** Lists researcher-facing workspace options. */
export const listExperimentWorkspaces = async (schoolId?: string) =>
  apiFetch<ExperimentWorkspaceOption[]>(
    `/experiments/workspaces${schoolId ? `?school_id=${schoolId}` : ""}`
  );

/** Lists lessons available inside a selected workspace. */
export const listExperimentWorkspaceLessons = async (workspaceId: string) =>
  apiFetch<ExperimentLessonOption[]>(
    `/experiments/workspaces/${workspaceId}/lessons`
  );

/** Lists approved baseline versions for a selected workspace lesson. */
export const listExperimentApprovedVersions = async (
  workspaceId: string,
  lessonPeriodId: string
) =>
  apiFetch<ExperimentApprovedVersion[]>(
    `/experiments/workspaces/${workspaceId}/lessons/${lessonPeriodId}/approved-versions`
  );

/** Persists focal learners for H2 generation. */
export const updateExperimentFocalLearners = async (
  experimentId: string,
  learnerIds: string[]
) =>
  apiFetch<ExperimentFocalLearnerSelectionPayload>(
    `/experiments/${experimentId}/focal-learners`,
    {
      method: "PUT",
      body: JSON.stringify({ learner_ids: learnerIds }),
    }
  );

/** Ends a study (research-manager action); returns the updated experiment. */
export const endExperiment = async (experimentId: string, endedBy = "researcher") =>
  apiFetch<ExperimentSummary>(`/experiments/${experimentId}/end`, {
    method: "POST",
    body: JSON.stringify({ ended_by: endedBy }),
  });

/** Marks/unmarks an experiment as a throwaway sandbox (never counts as real). */
export const setExperimentSandbox = async (experimentId: string, isSandbox: boolean) =>
  apiFetch<ExperimentSummary>(`/experiments/${experimentId}/sandbox`, {
    method: "POST",
    body: JSON.stringify({ is_sandbox: isSandbox }),
  });

/** Retries one FAILED H1 condition (research-admin) — regenerates just that pack. */
export const retryExperimentCondition = async (experimentId: string, conditionCode: string) =>
  apiFetch<ExperimentExecution>(
    `/experiments/${experimentId}/conditions/${encodeURIComponent(conditionCode)}/retry`,
    { method: "POST" }
  );

/** Fetches rater-rating progress for a study (results dashboard). */
export const getExperimentRatings = async (experimentId: string) =>
  apiFetch<ExperimentRatingsSummary>(
    `/evaluation/experiments/${experimentId}/ratings`
  );

/** Fetches H1/H2 hypothesis tests + inter-rater reliability for a study. */
export const getExperimentStatistics = async (experimentId: string) =>
  apiFetch<ExperimentStatistics>(
    `/evaluation/experiments/${experimentId}/statistics`
  );

/** Fetches the 7-phase / 18-row workflow snapshot (the Overview read model). */
export const getExperimentWorkflow = async (experimentId: string) =>
  apiFetch<import("./workflow").WorkflowSnapshot>(
    `/experiments/${experimentId}/workflow`
  );

/** Queues N synthetic LLM students to answer the lesson's diagnostic (seeds H2). */
export const triggerSyntheticStudents = async (experimentId: string, n: number) =>
  apiFetch<{ status: string; n: number }>(
    `/experiments/${experimentId}/synthetic-students?n=${n}`,
    { method: "POST" }
  );

/** Queues synthetic expert-teacher raters to score every packet of the experiment. */
export const triggerSyntheticRate = async (experimentId: string) =>
  apiFetch<{ status: string }>(`/experiments/${experimentId}/synthetic-rate`, {
    method: "POST",
  });

/** The configured default lesson context for the synthetic harness (a 3rd-term subtopic). */
export const getResearchDefaults = async () =>
  apiFetch<ResearchDefaults>("/experiments/research-defaults");

/** Queues the synthetic teacher to review/approve every pending pack (clears the C4 gate). */
export const triggerSyntheticTeacher = async (experimentId: string) =>
  apiFetch<{ status: string }>(`/experiments/${experimentId}/synthetic-teacher`, {
    method: "POST",
  });

/** Queues the full synthetic evaluation loop: teacher-review → export packets → rate. */
export const triggerSyntheticLoop = async (experimentId: string) =>
  apiFetch<{ status: string }>(`/experiments/${experimentId}/synthetic-loop`, {
    method: "POST",
  });

/** WebSocket URL for an experiment's live synthetic-test progress stream. */
export const syntheticProgressWsUrl = (experimentId: string) => {
  const base = API_BASE_URL.replace(/^http/, "ws");
  return `${base}/experiments/${experimentId}/synthetic/ws`;
};

/** Creates an investigation (an empty study; experiments are added afterwards). */
export const createInvestigation = async (payload: InvestigationCreateRequest) =>
  apiFetch<InvestigationDetail>("/experiments/investigations", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** Lists all investigations (studies). */
export const listInvestigations = async () =>
  apiFetch<InvestigationSummary[]>("/experiments/investigations");

/** Fetches one investigation with its scope lessons resolved. */
export const getInvestigation = async (investigationId: string) =>
  apiFetch<InvestigationDetail>(`/experiments/investigations/${investigationId}`);

/** Ends an investigation (research-manager action). */
export const endInvestigation = async (investigationId: string, endedBy = "researcher") =>
  apiFetch<InvestigationDetail>(`/experiments/investigations/${investigationId}/end`, {
    method: "POST",
    body: JSON.stringify({ ended_by: endedBy }),
  });

/** Rolled-up rater results across an investigation's experiments. */
export const getInvestigationResults = async (investigationId: string) =>
  apiFetch<InvestigationResultsRollup>(
    `/evaluation/investigations/${investigationId}/results`
  );

/** Bulk-imports offline rater ratings (research-manager action). */
export const importRatings = async (rows: RatingImportRow[]) =>
  apiFetch<RatingImportResult>("/evaluation/ratings/import", {
    method: "POST",
    body: JSON.stringify({ ratings: rows }),
  });

/** Fetches a study-pack manifest by artefact id (for the comparison view). */
export const getReviewPackManifest = async (
  artefactId: string
): Promise<ComparePackManifest> => {
  const response = await apiFetch<{ manifest: ComparePackManifest }>(
    `/artefacts/post-class-review-packs/${artefactId}`
  );
  return response.manifest;
};

/** Fetches a lesson's MCQ diagnostic (the questions the student took). */
export const getDiagnosticQuestions = async (
  planVersionId: string
): Promise<DiagnosticQuestions> =>
  apiFetch<DiagnosticQuestions>(
    `/assessments/exit-assessment/${encodeURIComponent(planVersionId)}/questions`
  );

/** Downloads the lesson plan as a WeasyPrint-rendered PDF (researcher export). */
export const downloadLessonPlanPdf = async (
  planVersionId: string
): Promise<{ blob: Blob; filename: string }> => {
  const { blob, response } = await apiFetchBlob(
    `/artefacts/lesson-plans/${encodeURIComponent(planVersionId)}/lesson-plan.pdf`
  );
  const disposition = response.headers.get("content-disposition") ?? "";
  const match = /filename="?([^"]+)"?/.exec(disposition);
  return { blob, filename: match?.[1] ?? `${planVersionId}-lesson-plan.pdf` };
};

/** Downloads one review pack (C0–C4 / P0–P1) as a WeasyPrint-rendered PDF. */
export const downloadPackPdf = async (
  artefactId: string
): Promise<{ blob: Blob; filename: string }> => {
  const { blob, response } = await apiFetchBlob(
    `/artefacts/post-class-review-packs/${encodeURIComponent(artefactId)}/pack.pdf`
  );
  const disposition = response.headers.get("content-disposition") ?? "";
  const match = /filename="?([^"]+)"?/.exec(disposition);
  return { blob, filename: match?.[1] ?? `${artefactId}-pack.pdf` };
};

/** Fetches an experiment's pipeline as an ordered, log-traceable story. */
export const getExperimentStory = async (
  experimentId: string
): Promise<ExperimentStory> =>
  apiFetch<ExperimentStory>(`/experiments/${encodeURIComponent(experimentId)}/story`);

/**
 * Teacher action: generate the class revision note for an accepted lesson (kicks
 * off the background build). Returns the refreshed experiment view.
 */
export const createReviewNote = async (experimentId: string): Promise<ExperimentSummary> =>
  apiFetch<ExperimentSummary>(
    `/experiments/${encodeURIComponent(experimentId)}/review-note`,
    { method: "POST" },
  );

/** Per-lesson assessment state for the lesson-prep queue. */
export type AssessmentStatus = {
  plan_version_id: string;
  has_assessment: boolean;
  released: boolean;
};

/**
 * Per-lesson assessment state (created? sent to students?) — one batched call,
 * so the lesson-prep queue can drive the create + send steps.
 */
export const listAssessmentStatus = async (
  planVersionIds: string[],
): Promise<AssessmentStatus[]> => {
  if (planVersionIds.length === 0) return [];
  const params = new URLSearchParams();
  for (const id of planVersionIds) params.append("plan_version_ids", id);
  return apiFetch<AssessmentStatus[]>(`/assessments/exit-assessment/status?${params.toString()}`);
};

/** Teacher action: release (send) the lesson's assessment to students. */
/**
 * Send the lesson's class test to students: approving its current version, so the approval
 * is kept. Refused if the questions changed since they were loaded.
 */
export const sendAssessment = async (planVersionId: string): Promise<ContentItem> => {
  const classTest = (await findContent(planVersionId)).find(
    (item) => item.type === "class-test",
  );
  if (!classTest) throw new Error("This lesson has no class test to send.");
  return approveContent(classTest.id, classTest.version);
};

/** One per-student revision note awaiting the teacher's approval (queue-count shape). */
export type PendingStudentNote = {
  artefact_id: string;
  plan_version_id: string;
  learner_id?: string | null;
};

/**
 * The teacher's pending per-student revision notes across all their lessons,
 * scoped server-side to the classes they teach. Used to light up the per-student
 * review steps on the lesson-prep queue (grouped by plan_version_id).
 */
export const listPendingStudentNotes = async (): Promise<PendingStudentNote[]> =>
  apiFetch<PendingStudentNote[]>("/artefacts/post-class-review-packs/pending");

