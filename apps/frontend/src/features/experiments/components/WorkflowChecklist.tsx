import { Link } from "@/shared/router";
import { formatRelativeTime } from "@/shared/utils/relativeTime";

import type {
  WorkflowItem,
  WorkflowPhase,
  WorkflowStatusKind,
  WorkflowSummary,
} from "../lib/workflow";

const STATUS_ICON: Record<WorkflowStatusKind, string> = {
  done: "✓",
  in_progress: "◐",
  ready: "○",
  pending: "☐",
  failed: "✗",
  not_applicable: "—",
};

const STATUS_TONE: Record<WorkflowStatusKind, string> = {
  done: "text-emerald-700",
  in_progress: "text-(--accent-deep)",
  ready: "text-(--accent-deep)",
  pending: "text-(--muted)",
  failed: "text-rose-700",
  not_applicable: "text-(--muted)",
};

function Row({ item, base }: { item: WorkflowItem; base: string }) {
  const detailBits = [item.count, formatRelativeTime(item.timestamp), item.reason].filter(
    Boolean,
  );
  const detail = detailBits.length ? detailBits.join(" · ") : null;
  const actionLabel = item.action_label ?? "Open";
  // Show the action button whenever the row has an href. Done rows now also
  // surface their button because the action is usually a *preview* of the
  // produced artefact (lesson plan, generated pack, assessment), not a CTA.
  const showAction = Boolean(item.href);
  const rowInner = (
    <>
      <span className="flex min-w-0 flex-1 items-baseline gap-3">
        <span
          className={`shrink-0 font-mono text-base leading-none ${STATUS_TONE[item.status]}`}
          aria-hidden
        >
          {STATUS_ICON[item.status]}
        </span>
        <span className="text-sm leading-relaxed text-(--ink)">{item.label}</span>
      </span>
      {detail ? (
        <span className="shrink-0 text-xs text-(--muted)" title={detail}>
          {detail}
        </span>
      ) : null}
      {showAction ? (
        item.status === "done" ? (
          // Done row → subtle "Preview" affordance (the action is informational,
          // not a call-to-action), so we render it as a ghost button.
          <span className="shrink-0 rounded-none border border-(--line) px-2.5 py-1 text-xs font-medium text-(--muted) transition group-hover:border-(--accent-deep) group-hover:text-(--accent-deep)">
            {actionLabel} →
          </span>
        ) : (
          // Ready / in_progress / pending → primary action affordance.
          <span className="shrink-0 rounded-none border border-(--accent-soft) bg-(--accent-soft)/40 px-2.5 py-1 text-xs font-semibold text-(--accent-deep) transition group-hover:bg-(--accent) group-hover:text-white">
            {actionLabel} →
          </span>
        )
      ) : null}
    </>
  );
  if (item.href) {
    return (
      <Link
        href={base + item.href}
        className="group flex items-baseline gap-3 border-b border-(--line) py-2.5 px-4 transition hover:bg-(--sunken) last:border-b-0"
      >
        {rowInner}
      </Link>
    );
  }
  return (
    <div className="flex items-baseline gap-3 border-b border-(--line) py-2.5 px-4 last:border-b-0">
      {rowInner}
    </div>
  );
}

/** Count how many items in a phase have reached `done`. */
function phaseProgress(phase: WorkflowPhase): { done: number; total: number } {
  return {
    done: phase.items.filter((item) => item.status === "done").length,
    total: phase.items.length,
  };
}

function PhaseAccordion({ phase, base }: { phase: WorkflowPhase; base: string }) {
  const { done, total } = phaseProgress(phase);
  const allDone = done === total;
  return (
    <details className="group border-b border-(--line) last:border-b-0" open={!allDone}>
      <summary className="flex cursor-pointer list-none items-baseline justify-between gap-3 bg-(--sunken)/50 px-4 py-3 hover:bg-(--sunken)">
        <div className="flex min-w-0 items-baseline gap-3">
          <span
            className="font-mono text-xs text-(--muted) transition-transform group-open:rotate-90"
            aria-hidden
          >
            ▸
          </span>
          <div className="min-w-0">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-(--muted)">
              {phase.title}
            </p>
            {phase.description ? (
              <p className="mt-0.5 text-xs leading-relaxed text-(--muted)">{phase.description}</p>
            ) : null}
          </div>
        </div>
        <p className="shrink-0 text-sm font-semibold tabular-nums">
          <span className={allDone ? "text-emerald-700" : "text-(--accent-deep)"}>{done}</span>
          <span className="text-(--muted)"> / {total}</span>
        </p>
      </summary>
      <div className="bg-white">
        {phase.items.map((item) => (
          <Row key={item.id} item={item} base={base} />
        ))}
      </div>
    </details>
  );
}

/**
 * Render the 18-row experiment workflow as a default-open-on-incomplete
 * accordion (collapsed phases that are fully done). A progress bar at the
 * top gives the visual rollup of the rollup; each phase header carries its
 * conceptual description so the researcher doesn't need a separate "what
 * does H1 mean" band on the page.
 */
export function WorkflowChecklist({
  phases,
  summary,
  base,
}: {
  phases: WorkflowPhase[];
  /** Pre-computed by the backend. Local fallback if the snapshot is still loading. */
  summary?: WorkflowSummary;
  base: string;
}) {
  const totalItems =
    summary?.total ?? phases.reduce((sum, phase) => sum + phase.items.length, 0);
  const doneItems =
    summary?.done ??
    phases.flatMap((phase) => phase.items).filter((item) => item.status === "done").length;
  const pct = summary?.pct ?? (totalItems === 0 ? 0 : Math.round((doneItems / totalItems) * 100));
  return (
    <section
      className="rounded-none border border-(--line) bg-white"
      aria-label="Experiment workflow"
    >
      <header className="space-y-3 px-4 py-3">
        <div className="flex items-baseline justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-(--muted)">
              Workflow
            </p>
            <p className="text-xs text-(--muted)">
              Eighteen steps grouped by phase — rows drill into the relevant tab.
            </p>
          </div>
          <p className="shrink-0 text-sm font-semibold tabular-nums">
            <span className="text-emerald-700">{doneItems}</span>
            <span className="text-(--muted)"> / {totalItems} done</span>
          </p>
        </div>
        <div
          className="h-1.5 w-full bg-(--sunken)"
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={`${doneItems} of ${totalItems} steps done`}
        >
          <div
            className="h-full bg-(--accent) transition-all"
            style={{ width: `${pct}%` }}
          />
        </div>
      </header>
      <div>
        {phases.map((phase) => (
          <PhaseAccordion key={phase.id} phase={phase} base={base} />
        ))}
      </div>
    </section>
  );
}
