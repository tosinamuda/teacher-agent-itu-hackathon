import { Card } from "@/shared/components/ui/Card";

import { ExperimentSummary, experimentSubtitle, experimentTitle } from "../lib/experiments";

type ExperimentDetailSummaryProps = {
  experiment: ExperimentSummary;
  executionCount: number;
};

const ReadinessPill = ({
  label,
  ready,
}: {
  label: string;
  ready: boolean;
}) => (
  <span
    className={`rounded-none px-3 py-1 text-xs font-semibold ${
      ready ? "bg-(--success-tint) text-(--success-ink)" : "bg-(--sunken) text-(--ink-2)"
    }`}
  >
    {label}: {ready ? "ready" : "blocked"}
  </span>
);

const StatCard = ({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) => (
  <Card padding="md" className="space-y-1">
    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
      {label}
    </p>
    <p className="text-lg font-semibold text-[color:var(--ink)]">{value}</p>
  </Card>
);

/** Renders the primary experiment summary with labels first and IDs second. */
export function ExperimentDetailSummary({
  experiment,
  executionCount,
}: ExperimentDetailSummaryProps) {
  return (
    <Card variant="glass" padding="lg" className="space-y-5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-2">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
            Experiment detail
          </div>
          <div>
            <h1 className="text-3xl font-semibold text-[color:var(--ink)]">
              {experimentTitle(experiment)}
            </h1>
            <p className="mt-2 text-sm font-semibold text-[color:var(--accent-deep)]">
              {experiment.experiment_code}
            </p>
            <p className="mt-1 text-sm text-[color:var(--muted)]">
              {experimentSubtitle(experiment) || experiment.workspace_name}
            </p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <ReadinessPill label="Lesson" ready={experiment.readiness.lesson_approved} />
          <ReadinessPill label="H1" ready={experiment.readiness.h1_ready} />
          <ReadinessPill label="H2" ready={experiment.readiness.h2_ready} />
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Workspace" value={experiment.workspace_name ?? "—"} />
        <StatCard label="Baseline" value={experiment.baseline_version_label ?? "—"} />
        <StatCard label="Executions" value={executionCount} />
        <StatCard label="Teacher" value={experiment.teacher_name ?? "—"} />
      </div>

      <div className="rounded-3xl border border-[color:var(--line)] bg-(--surface) p-4">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
          Research details
        </p>
        <div className="mt-3 grid gap-2 text-sm text-[color:var(--muted)] md:grid-cols-2">
          <p>Experiment ID: {experiment.experiment_id}</p>
          <p>Workspace ID: {experiment.teacher_workspace_id}</p>
          <p>Plan version ID: {experiment.plan_version_id ?? "Not yet authored"}</p>
          <p>Lesson period ID: {experiment.lesson_period_id ?? "—"}</p>
        </div>
      </div>
    </Card>
  );
}
