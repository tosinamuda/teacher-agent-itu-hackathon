import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";
import { Link } from "@/shared/router";

import type { ExecutionRow } from "../api";

const STATUS_FILTERS = ["all", "queued", "running", "succeeded", "failed", "created"] as const;
const RECOVERABLE = new Set(["queued", "failed", "created"]);
const STOPPABLE = new Set(["queued", "running", "created"]);

/** The coloured pill an execution's status reads as. */
function StatusBadge({ status }: { status: string }) {
  const tone =
    status === "succeeded"
      ? "bg-(--sunken) text-(--success-ink)"
      : status === "failed"
        ? "bg-(--danger-tint) text-(--danger-ink)"
        : status === "running" || status === "queued"
          ? "bg-(--accent-soft) text-(--accent-deep)"
          : "bg-(--sunken) text-(--muted)";
  return (
    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${tone}`}>
      {status}
    </span>
  );
}

/** Recent experiment executions, filtered by status, with re-dispatch and cancel. */
export function ExecutionsCard({
  rows,
  isLoading,
  statusFilter,
  onStatusFilter,
  onRedispatch,
  onCancel,
  isRedispatching,
  isCancelling,
}: {
  rows: ExecutionRow[];
  isLoading: boolean;
  statusFilter: string;
  onStatusFilter: (status: string) => void;
  onRedispatch: (executionId: string) => void;
  onCancel: (executionId: string) => void;
  isRedispatching: boolean;
  isCancelling: boolean;
}) {
  return (
    <Card padding="md" className="space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-(--muted)">Executions</h2>
        <div className="flex flex-wrap gap-1">
          {STATUS_FILTERS.map((s) => (
            <button
              key={s}
              onClick={() => onStatusFilter(s)}
              className={`rounded-full px-3 py-1 text-xs ${
                statusFilter === s
                  ? "bg-(--accent) text-white"
                  : "bg-(--sunken) text-(--muted) hover:text-(--ink)"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>
      {isLoading && <p className="text-sm text-(--muted)">Loading…</p>}
      {!isLoading && rows.length === 0 && (
        <p className="text-sm text-(--muted)">No executions for this filter.</p>
      )}
      {rows.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-(--muted)">
              <tr>
                <th className="py-1 pr-4">Experiment</th>
                <th className="py-1 pr-4">H</th>
                <th className="py-1 pr-4">Status</th>
                <th className="py-1 pr-4">Error</th>
                <th className="py-1 pr-4" />
              </tr>
            </thead>
            <tbody>
              {rows.map((e) => (
                <tr key={e.execution_id} className="border-t border-(--line) align-top">
                  <td className="py-2 pr-4">
                    <Link
                      href={`/research/experiments/${e.experiment_id}/results`}
                      className="font-medium text-(--accent) hover:underline"
                    >
                      {e.experiment_code}
                    </Link>
                    <div className="font-mono text-xs text-(--muted)">{e.execution_id}</div>
                  </td>
                  <td className="py-2 pr-4">{e.hypothesis}</td>
                  <td className="py-2 pr-4">
                    <StatusBadge status={e.status} />
                  </td>
                  <td className="py-2 pr-4 max-w-xs text-xs text-(--muted)">
                    {e.error_category ? (
                      <span title={e.error_message ?? ""}>{e.error_category}</span>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td className="py-2 pr-4 text-right">
                    <div className="flex justify-end gap-2">
                      {RECOVERABLE.has(e.status) && (
                        <Button
                          variant="secondary"
                          size="sm"
                          disabled={isRedispatching}
                          onClick={() => onRedispatch(e.execution_id)}
                        >
                          Re-dispatch
                        </Button>
                      )}
                      {STOPPABLE.has(e.status) && (
                        <Button
                          variant="danger"
                          size="sm"
                          disabled={isCancelling}
                          onClick={() => {
                            if (window.confirm(`Cancel execution ${e.execution_id}?`)) {
                              onCancel(e.execution_id);
                            }
                          }}
                        >
                          Cancel
                        </Button>
                      )}
                    </div>
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
