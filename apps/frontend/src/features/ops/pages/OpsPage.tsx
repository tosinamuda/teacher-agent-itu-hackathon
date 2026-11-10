import { useState } from "react";

import { ExecutionsCard } from "../components/ExecutionsCard";
import { JobQueueCard } from "../components/JobQueueCard";
import { JobsCard } from "../components/JobsCard";
import { useOpsActions, useOpsExecutions, useOpsHealth, useOpsJobs } from "../hooks/useOps";

const all = (filter: string) => (filter === "all" ? null : filter);

/** Composition root for the operations panel: the job queue, its jobs, execution recovery. */
export function OpsPage() {
  const health = useOpsHealth();
  const [jobFilter, setJobFilter] = useState<string>("all");
  const jobs = useOpsJobs(all(jobFilter));
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const executions = useOpsExecutions(all(statusFilter));
  const { cancelJob, redispatch, cancel } = useOpsActions();

  return (
    <main className="flex w-full flex-col gap-4 py-4">
      <header className="max-w-3xl space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight text-(--ink)">Operations</h1>
        <p className="text-sm text-(--muted)">
          Background jobs, the runners taking them, and experiment-execution recovery.
          Auto-refreshes every few seconds.
        </p>
      </header>

      <JobQueueCard health={health.data} isLoading={health.isLoading} isError={health.isError} />

      <JobsCard
        rows={jobs.data ?? []}
        isLoading={jobs.isLoading}
        stateFilter={jobFilter}
        onStateFilter={setJobFilter}
        onCancel={(jobId) => cancelJob.mutate(jobId)}
        isCancelling={cancelJob.isPending}
      />

      <ExecutionsCard
        rows={executions.data ?? []}
        isLoading={executions.isLoading}
        statusFilter={statusFilter}
        onStatusFilter={setStatusFilter}
        onRedispatch={(executionId) => redispatch.mutate(executionId)}
        onCancel={(executionId) => cancel.mutate(executionId)}
        isRedispatching={redispatch.isPending}
        isCancelling={cancel.isPending}
      />
    </main>
  );
}
