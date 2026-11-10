import { Badge } from "@/shared/components/ui/Badge";

import { ExperimentExecution } from "../lib/experiments";

/** A labelled metric tile. */
function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-2xl border border-(--line) bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-(--muted)">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-(--ink)">{value}</p>
    </div>
  );
}

/**
 * Outcome summary for the latest execution: generation status distribution +
 * how many condition runs, focal cases and blinded packets it produced.
 */
export function ResearchResultsSummary({
  execution,
}: {
  execution: ExperimentExecution | undefined;
}) {
  if (!execution) {
    return (
      <p className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-6 text-center text-sm text-(--muted)">
        No executions yet — run H1 or H2 to produce results.
      </p>
    );
  }

  const runs = execution.condition_runs ?? [];
  const statusCounts = runs.reduce<Record<string, number>>((acc, run) => {
    acc[run.status] = (acc[run.status] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2 text-sm text-(--muted)">
        <span className="font-semibold text-(--ink)">Latest execution</span>
        <Badge variant="outline">{execution.hypothesis}</Badge>
        <Badge variant="accent">{execution.status}</Badge>
        <span>attempt {execution.attempt_number}</span>
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        <Stat label="Condition runs" value={runs.length} />
        <Stat label="Focal cases" value={execution.focal_cases?.length ?? 0} />
        <Stat label="Blinded packets" value={execution.packets?.length ?? 0} />
      </div>

      {runs.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {Object.entries(statusCounts).map(([status, count]) => (
            <span
              key={status}
              className="rounded-none border border-(--line) px-3 py-1 text-xs text-(--muted)"
            >
              {status}: <span className="font-semibold text-(--ink)">{count}</span>
            </span>
          ))}
        </div>
      ) : null}
    </div>
  );
}
