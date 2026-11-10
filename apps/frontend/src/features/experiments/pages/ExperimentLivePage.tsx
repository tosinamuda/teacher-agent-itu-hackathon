import { useExperiment } from "../hooks/useExperiments";
import { useSyntheticLog } from "../hooks/useSyntheticLog";

const FLOW_LABEL: Record<string, string> = {
  generation: "generation",
  teacher_review: "teacher",
  students: "students",
  ratings: "ratings",
  loop: "loop",
};

/** Live tab: the realtime event stream of a running synthetic test. */
export default function ExperimentLivePage({ experimentId }: { experimentId: string }) {
  const { entries, connected } = useSyntheticLog(experimentId);
  const ended = useExperiment(experimentId).data?.lifecycle_status === "ended";
  if (ended) {
    return <p className="py-6 text-sm text-(--muted)">Nothing runs on an ended experiment.</p>;
  }

  return (
    <div className="space-y-3 py-6">
      <div className="flex items-center gap-2 text-sm">
        <span
          className={`h-2.5 w-2.5 rounded-none ${
            connected ? "animate-pulse bg-(--success)" : "bg-(--line)"
          }`}
        />
        <span className="text-(--muted)">
          {connected ? "Streaming" : "Connecting…"}
        </span>
      </div>

      {entries.length === 0 ? (
        <p className="py-6 text-sm text-(--muted)">No activity yet. Runs started on Test show here.</p>
      ) : (
        <div className="max-h-[30rem] space-y-1 overflow-y-auto rounded-2xl border border-(--line) bg-(--surface) p-3 text-xs">
          {entries.map((entry, index) => (
            <div key={index} className="flex items-baseline gap-3">
              <span className="w-20 shrink-0 font-semibold text-(--accent-deep)">
                {FLOW_LABEL[entry.flow] ?? entry.flow}
              </span>
              <span className="w-12 shrink-0 text-right text-(--muted)">
                {entry.total ? `${entry.done ?? 0}/${entry.total}` : entry.type}
              </span>
              <span className={entry.type === "error" ? "text-(--danger)" : "text-(--ink)"}>
                {entry.message ?? entry.type}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
