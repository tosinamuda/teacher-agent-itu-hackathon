import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { ExperimentExecution, executionStatusTone } from "../lib/experiments";
import {
  executionErrorMessage,
  shortExecutionId,
} from "../services/executionError";

const STATUS_BADGE_CLASS: Record<string, string> = {
  danger: "bg-(--danger-tint) text-(--danger-ink)",
  warning: "bg-(--warning-tint) text-(--warning-ink)",
  success: "bg-(--success-tint) text-(--success-ink)",
};

type ExperimentExecutionHistoryProps = {
  executions: ExperimentExecution[];
  selectedExecutionId: string | null;
  onSelect: (executionId: string) => void;
  title?: string;
  backHref?: string;
};

export function ExperimentExecutionHistory({
  executions,
  selectedExecutionId,
  onSelect,
  title = "Attempts by hypothesis",
  backHref,
}: ExperimentExecutionHistoryProps) {
  return (
    <Card padding="lg">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
            Execution history
          </p>
          <h3 className="text-lg font-semibold text-[color:var(--ink)]">
            {title}
          </h3>
        </div>
        <span className="text-sm text-[color:var(--muted)]">{executions.length} executions</span>
      </div>

      {executions.length === 0 ? (
        <p className="text-sm text-[color:var(--muted)]">
          No executions have been launched yet.
        </p>
      ) : (
        <div className="space-y-3">
          {executions.map((execution) => {
            const active = execution.execution_id === selectedExecutionId;
            const tone = executionStatusTone(execution.status);
            const badgeClass = STATUS_BADGE_CLASS[tone] ?? "bg-(--sunken) text-(--ink-2)";
            // Whether to show an error block is driven by status, not by the
            // presence/content of the raw message.
            const errorMessage = executionErrorMessage(execution);
            return (
              <div
                key={execution.execution_id}
                className={`w-full rounded-2xl border transition ${
                  active
                    ? "border-[color:var(--accent)] bg-[color:var(--accent-soft)]"
                    : "border-[color:var(--line)] bg-(--surface)"
                }`}
              >
                {/* Clickable header selects this execution. Kept as its own
                    button so the error disclosure below (interactive) isn't
                    nested inside another interactive element. */}
                <button
                  type="button"
                  onClick={() => onSelect(execution.execution_id)}
                  className="flex w-full flex-wrap items-center justify-between gap-3 px-4 py-3 text-left"
                >
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-[color:var(--ink)]">
                      {execution.hypothesis} · Attempt {execution.attempt_number}
                    </p>
                    <p
                      className="font-mono text-xs text-[color:var(--muted)]"
                      title={execution.execution_id}
                    >
                      {shortExecutionId(execution.execution_id)}
                    </p>
                  </div>
                  <span
                    className={`rounded-none px-3 py-1 text-xs font-semibold capitalize ${badgeClass}`}
                  >
                    {execution.status}
                  </span>
                </button>
                <div className="px-4 pb-3 text-xs text-[color:var(--muted)]">
                  <div className="flex flex-wrap items-center gap-3">
                    <span>Focal cases: {execution.focal_cases?.length ?? 0}</span>
                  </div>
                  {errorMessage ? (
                    <div className="mt-2 space-y-1">
                      <p className="text-[color:var(--danger-ink)]">{errorMessage}</p>
                      {execution.error_message ? (
                        <details>
                          <summary className="cursor-pointer text-[color:var(--muted)]">
                            Technical details
                          </summary>
                          <pre className="mt-1 max-h-48 overflow-auto whitespace-pre-wrap break-words rounded-none border border-[color:var(--line)] bg-(--sunken) p-2 font-mono text-[11px] text-[color:var(--ink-2)]">
                            {execution.error_message}
                          </pre>
                        </details>
                      ) : null}
                    </div>
                  ) : null}
                </div>
              </div>
            );
          })}
          {backHref && (
            <div className="pt-2">
              <Link
                className="text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
                href={backHref}
              >
                Back to list
              </Link>
            </div>
          )}
        </div>
      )}
    </Card>
  );
}
