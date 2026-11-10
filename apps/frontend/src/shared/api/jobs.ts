import { apiFetch } from "@/shared/api/client";

/** A background job as the caller who asked for it follows it. */
export type JobStatus = {
  job_id: string;
  kind: string;
  subject: string | null;
  state: "queued" | "running" | "succeeded" | "failed" | "cancelled";
  attempts: number;
  error: string | null;
  result: Record<string, unknown> | null;
  created_at: string | null;
  finished_at: string | null;
};

/** What a request that queues work answers with: the job to follow. */
export type JobAccepted = { job_id: string };

const POLL_MS = 1500;

export const getJob = (jobId: string): Promise<JobStatus> =>
  apiFetch<JobStatus>(`/jobs/${encodeURIComponent(jobId)}`);

/** The newest job of this kind for the subject that the caller asked for, or null. */
export const latestJob = (kind: string, subject: string): Promise<JobStatus | null> =>
  apiFetch<JobStatus | null>(
    `/jobs?${new URLSearchParams({ kind, subject }).toString()}`,
  );

export function isUnfinished(job: JobStatus | null | undefined): boolean {
  return job?.state === "queued" || job?.state === "running";
}

/**
 * Wait for a job to end: its result when it succeeds, an error when it does not.
 *
 * The error carries the job's reason as `{"detail": …}`, the shape a refused request has,
 * so the pages that read a request's error read a job's the same way.
 */
export async function awaitJob<R>(jobId: string): Promise<R> {
  for (;;) {
    const job = await getJob(jobId);
    if (job.state === "succeeded") return job.result as R;
    if (job.state === "failed" || job.state === "cancelled") {
      throw new Error(JSON.stringify({ detail: job.error ?? `job_${job.state}` }));
    }
    await new Promise((resolve) => setTimeout(resolve, POLL_MS));
  }
}

/** Queue work and wait for what it made. */
export async function runJob<R>(submit: () => Promise<JobAccepted>): Promise<R> {
  const { job_id } = await submit();
  return awaitJob<R>(job_id);
}
