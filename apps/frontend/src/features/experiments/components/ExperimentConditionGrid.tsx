import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { ExperimentConditionRun } from "../lib/experiments";
import { conditionErrorSummary } from "../services/executionError";

type ExperimentConditionGridProps = {
  runs: ExperimentConditionRun[];
  /** Used to build per-pack preview drill-in links (e.g. `/research/experiments/{id}/c0`). */
  experimentBaseHref: string;
  /** The study draw these runs belong to; its preview links open that draw. */
  draw?: number;
  /** Research-admin retry of one FAILED condition. Omit to hide retry (e.g. teacher view). */
  onRetry?: (conditionCode: string) => void;
  /** The condition currently retrying (its button shows a spinner/disabled). */
  retryingCode?: string | null;
  /** Export one pack's PDF. Omit to hide per-pack export. */
  onExportPack?: (artefactId: string) => void;
  /** The artefact currently exporting (its button shows a spinner/disabled). */
  exportingArtefactId?: string | null;
  /** Whether the teacher has approved C4's pack, which ends its gate. */
  c4Approved?: boolean;
};

/** Conditions whose pack has a dedicated researcher preview route. */
const PREVIEWABLE = new Set(["C0", "C1", "C2", "C3"]);

const isSucceeded = (status: string) => /succeed|complete|done/i.test(status);

const chipClass = (status: string, gated: boolean): string => {
  if (gated) return "bg-(--warning-tint) text-(--warning-ink)";
  const value = status.toLowerCase();
  if (value.includes("fail")) return "bg-(--danger-tint) text-(--danger-ink)";
  if (value.includes("succeed") || value.includes("complete")) {
    return "bg-(--success-tint) text-(--success-ink)";
  }
  if (value.includes("run") || value.includes("queue")) {
    return "bg-(--warning-tint) text-(--warning-ink)";
  }
  return "bg-(--sunken) text-(--ink-2)";
};

/** Short id (`AT-xxxxxx…xxxx`); full id on hover via `title`. */
function shortId(id: string | null | undefined): string {
  if (!id) return "—";
  if (id.length <= 13) return id;
  return `${id.slice(0, 7)}…${id.slice(-4)}`;
}

/**
 * One row per condition (C0–C4) in a table (design-system `.tbl` style):
 * status chip, the produced pack id, and per-row actions (preview / export /
 * retry). A re-run or retry can leave more than one run per code — we keep the
 * SUCCEEDED run (a condition with a valid pack is done), else the latest.
 */
export function ExperimentConditionGrid({
  runs,
  experimentBaseHref,
  draw,
  onRetry,
  retryingCode,
  onExportPack,
  exportingArtefactId,
  c4Approved = false,
}: ExperimentConditionGridProps) {
  const byCode = new Map<string, ExperimentConditionRun>();
  for (const run of runs) {
    const existing = byCode.get(run.condition_code);
    if (!existing || isSucceeded(run.status) || !isSucceeded(existing.status)) {
      byCode.set(run.condition_code, run);
    }
  }
  const uniqueRuns = [...byCode.values()].sort((a, b) =>
    a.condition_code.localeCompare(b.condition_code)
  );

  if (uniqueRuns.length === 0) {
    return (
      <Card padding="lg">
        <p className="text-sm text-[color:var(--muted)]">
          No condition runs yet — generate C0–C4 to populate this.
        </p>
      </Card>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="text-left text-[11px] font-medium uppercase tracking-[0.08em] text-(--muted)">
            <th className="border-b border-(--line) px-2 pb-3.5">Condition</th>
            <th className="border-b border-(--line) px-2 pb-3.5">Status</th>
            <th className="border-b border-(--line) px-2 pb-3.5">Pack</th>
            <th className="border-b border-(--line) px-2 pb-3.5 text-right">Action</th>
          </tr>
        </thead>
        <tbody>
          {uniqueRuns.map((run) => {
            const code = run.condition_code;
            const isC4 = code.toUpperCase() === "C4";
            const isFailed = run.status.toLowerCase().includes("fail");
            const atTheGate = isC4 && !isFailed && !c4Approved;
            const previewHref = PREVIEWABLE.has(code.toUpperCase())
              ? `${experimentBaseHref}/${code.toLowerCase()}${draw ? `?draw=${draw}` : ""}`
              : null;
            return (
              <tr key={run.condition_run_id} className="border-b border-(--line) align-top last:border-0">
                <td className="px-2 py-4 font-semibold text-(--ink)">{code}</td>
                <td className="px-2 py-4">
                  <span
                    className={`inline-flex rounded-none px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-[0.06em] ${chipClass(run.status, atTheGate)}`}
                  >
                    {atTheGate ? "Teacher gate" : isC4 && c4Approved ? "Teacher approved" : run.status}
                  </span>
                  {isFailed ? (
                    <div className="mt-1.5 max-w-[36ch] text-[11px] text-(--danger-ink)">
                      {conditionErrorSummary(run.error_message)}
                      {run.error_message ? (
                        <details className="mt-0.5">
                          <summary className="cursor-pointer text-(--muted)">Technical details</summary>
                          <p className="mt-1 break-words font-mono text-[10px] text-(--muted)">
                            {run.error_message}
                          </p>
                        </details>
                      ) : null}
                    </div>
                  ) : null}
                </td>
                <td
                  className="px-2 py-4 font-mono text-xs text-(--muted)"
                  title={run.artefact_id ?? undefined}
                >
                  {shortId(run.artefact_id)}
                </td>
                <td className="px-2 py-4 text-right">
                  <div className="flex flex-wrap items-center justify-end gap-x-4 gap-y-1">
                    {isFailed && onRetry ? (
                      <button
                        type="button"
                        onClick={() => onRetry(code)}
                        disabled={retryingCode === code}
                        className="text-xs font-semibold text-(--danger-ink) underline hover:no-underline disabled:opacity-60"
                      >
                        {retryingCode === code ? "Retrying…" : `Retry ${code}`}
                      </button>
                    ) : null}
                    {previewHref && !isFailed ? (
                      <Link
                        href={previewHref}
                        className="text-xs font-semibold text-(--accent-deep) hover:underline"
                      >
                        Preview {code} →
                      </Link>
                    ) : null}
                    {isC4 && !isFailed ? (
                      <span className="text-[11px] italic text-(--muted)">Review on Results</span>
                    ) : null}
                    {onExportPack && run.artefact_id && !isFailed ? (
                      <button
                        type="button"
                        onClick={() => onExportPack(run.artefact_id as string)}
                        disabled={exportingArtefactId === run.artefact_id}
                        className="text-xs text-(--muted) underline hover:text-(--ink) disabled:opacity-60"
                      >
                        {exportingArtefactId === run.artefact_id ? "Exporting…" : "Export PDF"}
                      </button>
                    ) : null}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
