import { Card } from "@/shared/components/ui/Card";

import type { JobState, OpsHealth } from "../api";
import { readQueueHealth } from "../services/queueHealth";

const TONE_DOT = {
  ok: "bg-(--success-ink)",
  warn: "bg-(--accent)",
  danger: "bg-(--danger-ink)",
} as const;

const TONE_TEXT = {
  ok: "text-(--ink)",
  warn: "text-(--ink)",
  danger: "text-(--danger-ink)",
} as const;

const STATES: JobState[] = ["queued", "running", "failed", "succeeded", "cancelled"];

/** Whether jobs are being run: the verdict, the runners behind it, and the queue by state. */
export function JobQueueCard({
  health,
  isLoading,
  isError,
}: {
  health: OpsHealth | undefined;
  isLoading: boolean;
  isError: boolean;
}) {
  return (
    <Card padding="md" className="space-y-3">
      <h2 className="text-sm font-semibold uppercase tracking-wide text-(--muted)">Job queue</h2>
      {isLoading && <p className="text-sm text-(--muted)">Loading…</p>}
      {isError && <p className="text-sm text-(--danger-ink)">Failed to reach the ops API.</p>}
      {health && <QueueDetail health={health} />}
    </Card>
  );
}

function QueueDetail({ health }: { health: OpsHealth }) {
  const verdict = readQueueHealth(health);
  return (
    <>
      <div className="space-y-1">
        <div className="flex items-center gap-2 text-sm">
          <span className={`inline-block h-2 w-2 rounded-full ${TONE_DOT[verdict.tone]}`} />
          <span className={`font-medium ${TONE_TEXT[verdict.tone]}`}>{verdict.headline}</span>
        </div>
        <p className="text-sm text-(--muted)">{verdict.detail}</p>
      </div>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:gap-8">
        <div className="space-y-1">
          <p className="text-xs font-medium text-(--muted)">Runners</p>
          {health.runners.length === 0 && (
            <p className="text-sm text-(--muted)">None has reported yet.</p>
          )}
          {health.runners.map((runner) => (
            <div key={runner.runner} className="flex items-center gap-2 text-sm">
              <span
                className={`inline-block h-2 w-2 rounded-full ${runner.online ? "bg-(--success-ink)" : "bg-(--line)"}`}
              />
              <span className="font-mono text-xs text-(--ink)">{runner.runner}</span>
              <span className="text-(--muted)">
                {runner.online ? `${runner.running}/${runner.slots} running` : "gone"}
              </span>
            </div>
          ))}
        </div>
        <div className="space-y-1">
          <p className="text-xs font-medium text-(--muted)">Jobs</p>
          <div className="flex flex-wrap gap-x-4 gap-y-1 text-sm">
            {STATES.map((state) => (
              <span key={state} className="text-(--muted)">
                {state} <span className="font-medium text-(--ink)">{health.counts[state]}</span>
              </span>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
