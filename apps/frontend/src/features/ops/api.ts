import { apiFetch } from "@/shared/api/client";

/** A process running jobs, as it last reported itself. */
export type RunnerInfo = {
  runner: string;
  online: boolean;
  slots: number;
  running: number;
  started_at: string | null;
  seen_at: string | null;
};

export type JobState = "queued" | "running" | "succeeded" | "failed" | "cancelled";

/** Whether jobs are being run: the runners seen, and what is waiting on them. */
export type OpsHealth = {
  runners: RunnerInfo[];
  counts: Record<JobState, number>;
  oldest_queued_age_seconds: number | null;
  slots_per_runner: number;
};

export type JobRow = {
  job_id: string;
  kind: string;
  subject: string | null;
  state: JobState;
  attempts: number;
  runner: string | null;
  last_error: string | null;
  created_at: string | null;
  started_at: string | null;
  finished_at: string | null;
};

export type ExecutionRow = {
  execution_id: string;
  experiment_id: string;
  experiment_code: string;
  hypothesis: string;
  status: string;
  attempt_number: number;
  error_category: string | null;
  error_message: string | null;
  created_at: string | null;
  updated_at: string | null;
};

export type OpsActionResponse = {
  ok: boolean;
  detail?: string | null;
  execution_id?: string | null;
  status?: string | null;
  cancelled_job_ids?: string[];
};

const post = (path: string) =>
  apiFetch<OpsActionResponse>(path, { method: "POST" });

function query(params: Record<string, string | null | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) if (value) search.set(key, value);
  return search.toString();
}

export const opsApi = {
  health: () => apiFetch<OpsHealth>("/ops/health"),
  jobs: (state?: string | null, limit = 50) =>
    apiFetch<JobRow[]>(`/ops/jobs?${query({ state, limit: String(limit) })}`),
  executions: (status?: string | null, limit = 50) =>
    apiFetch<ExecutionRow[]>(`/ops/executions?${query({ status, limit: String(limit) })}`),
  cancelJob: (jobId: string) => post(`/ops/jobs/${encodeURIComponent(jobId)}/cancel`),
  redispatch: (executionId: string) =>
    post(`/ops/executions/${encodeURIComponent(executionId)}/redispatch`),
  cancel: (executionId: string) =>
    post(`/ops/executions/${encodeURIComponent(executionId)}/cancel`),
};
