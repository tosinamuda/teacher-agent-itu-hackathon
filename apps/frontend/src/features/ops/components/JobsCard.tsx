import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import type { JobRow } from "../api";

const STATE_FILTERS = ["all", "queued", "running", "failed", "succeeded", "cancelled"] as const;
const UNFINISHED = new Set(["queued", "running"]);

function StateBadge({ state }: { state: string }) {
  const tone =
    state === "succeeded"
      ? "bg-(--sunken) text-(--success-ink)"
      : state === "failed"
        ? "bg-(--danger-tint) text-(--danger-ink)"
        : UNFINISHED.has(state)
          ? "bg-(--accent-soft) text-(--accent-deep)"
          : "bg-(--sunken) text-(--muted)";
  return (
    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${tone}`}>
      {state}
    </span>
  );
}

/** Background jobs, unfinished first: what each acts on, its runs, and why it last stopped. */
export function JobsCard({
  rows,
  isLoading,
  stateFilter,
  onStateFilter,
  onCancel,
  isCancelling,
}: {
  rows: JobRow[];
  isLoading: boolean;
  stateFilter: string;
  onStateFilter: (state: string) => void;
  onCancel: (jobId: string) => void;
  isCancelling: boolean;
}) {
  return (
    <Card padding="md" className="space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-(--muted)">Jobs</h2>
        <div className="flex flex-wrap gap-1">
          {STATE_FILTERS.map((state) => (
            <button
              key={state}
              onClick={() => onStateFilter(state)}
              className={`rounded-full px-3 py-1 text-xs ${
                stateFilter === state
                  ? "bg-(--accent) text-white"
                  : "bg-(--sunken) text-(--muted) hover:text-(--ink)"
              }`}
            >
              {state}
            </button>
          ))}
        </div>
      </div>
      {isLoading && <p className="text-sm text-(--muted)">Loading…</p>}
      {!isLoading && rows.length === 0 && (
        <p className="text-sm text-(--muted)">No jobs for this filter.</p>
      )}
      {rows.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-(--muted)">
              <tr>
                <th className="py-1 pr-4">Job</th>
                <th className="py-1 pr-4">State</th>
                <th className="py-1 pr-4">Runs</th>
                <th className="py-1 pr-4">Last error</th>
                <th className="py-1 pr-4" />
              </tr>
            </thead>
            <tbody>
              {rows.map((job) => (
                <tr key={job.job_id} className="border-t border-(--line) align-top">
                  <td className="py-2 pr-4">
                    <div className="font-mono text-xs text-(--ink)">{job.kind}</div>
                    <div className="font-mono text-xs text-(--muted)">{job.subject ?? job.job_id}</div>
                  </td>
                  <td className="py-2 pr-4">
                    <StateBadge state={job.state} />
                  </td>
                  <td className="py-2 pr-4">{job.attempts}</td>
                  <td className="py-2 pr-4 max-w-xs text-xs text-(--muted)">
                    {job.last_error ?? "—"}
                  </td>
                  <td className="py-2 pr-4 text-right">
                    {UNFINISHED.has(job.state) && (
                      <Button
                        variant="danger"
                        size="sm"
                        disabled={isCancelling}
                        onClick={() => {
                          if (window.confirm(`Cancel ${job.kind} ${job.subject ?? job.job_id}?`)) {
                            onCancel(job.job_id);
                          }
                        }}
                      >
                        Cancel
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
}
