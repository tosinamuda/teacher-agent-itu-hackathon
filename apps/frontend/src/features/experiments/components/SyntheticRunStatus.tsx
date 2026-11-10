import { SyntheticProgressState } from "../hooks/useSyntheticProgress";
import { SyntheticProgressEvent } from "../lib/experiments";

const FLOW_LABELS: Record<string, string> = {
  loop: "Full loop",
  generation: "Study-pack generation",
  teacher_review: "Teacher review",
  students: "Synthetic students",
  ratings: "Expert ratings",
};
// Priority when several flows have events: the orchestrated loop wins, then the
// most "downstream" stage. Used to pick which flow to feature prominently.
const FLOW_ORDER = ["loop", "ratings", "teacher_review", "students", "generation"] as const;

const pctOf = (event: SyntheticProgressEvent): number => {
  const total = event.total ?? 0;
  const done = event.done ?? 0;
  if (total > 0) return Math.min(100, Math.round((done / total) * 100));
  return event.type === "done" ? 100 : 8;
};

const statusWord = (event: SyntheticProgressEvent): string => {
  if (event.type === "error") return "failed";
  if (event.type === "done") return "done";
  const total = event.total ?? 0;
  return total > 0 ? `${event.done ?? 0}/${total}` : "running…";
};

/**
 * One prominent, always-present status block for the synthetic harness. Features the
 * currently-running flow (or the latest one) with a progress bar + live message, and
 * shows compact chips for the other flows so the whole run's progress is visible at a
 * glance — driven by the per-flow WebSocket events.
 */
export function SyntheticRunStatus({ progress }: { progress: SyntheticProgressState }) {
  const present: { key: string; event: SyntheticProgressEvent }[] = [];
  for (const key of FLOW_ORDER) {
    const event = progress[key];
    if (event) present.push({ key, event });
  }

  if (present.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-(--line) bg-(--panel)/40 px-3 py-3 text-[11px] text-(--muted)">
        No synthetic run yet. Start at step 2 (Generate study packs), or click{" "}
        <span className="font-semibold">Run full synthetic loop</span>. Live progress shows here.
      </div>
    );
  }

  const running = present.find((entry) => entry.event.type === "progress" || entry.event.type === "start");
  const featured = running ?? present[present.length - 1];
  const event = featured.event;
  const isError = event.type === "error";
  const isDone = event.type === "done";
  const barColor = isError ? "bg-(--danger-tint)0" : isDone ? "bg-(--success-tint)0" : "bg-(--accent)";
  const dotColor = isError ? "bg-(--danger-tint)0" : isDone ? "bg-(--success-tint)0" : "bg-(--accent) animate-pulse";

  return (
    <div className="space-y-2 rounded-xl border border-(--line) bg-(--panel)/50 px-3 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className={`h-2.5 w-2.5 rounded-none ${dotColor}`} />
          <span className="text-xs font-semibold text-(--ink)">
            {FLOW_LABELS[featured.key] ?? featured.key}
          </span>
          <span className="text-[11px] text-(--muted)">{statusWord(event)}</span>
        </div>
        <div className="flex gap-1">
          {present
            .filter((entry) => entry.key !== featured.key)
            .map((entry) => (
              <span
                key={entry.key}
                className="rounded-none bg-(--line)/60 px-2 py-0.5 text-[10px] text-(--muted)"
              >
                {FLOW_LABELS[entry.key] ?? entry.key}: {statusWord(entry.event)}
              </span>
            ))}
        </div>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-none bg-(--line)">
        <div
          className={`h-full rounded-none transition-all ${barColor}`}
          style={{ width: `${pctOf(event)}%` }}
        />
      </div>
      {event.message ? (
        <p className={`text-[11px] ${isError ? "text-(--danger)" : "text-(--muted)"}`}>
          {event.message}
        </p>
      ) : null}
    </div>
  );
}
