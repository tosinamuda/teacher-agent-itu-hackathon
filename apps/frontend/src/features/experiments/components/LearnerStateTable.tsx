import { ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { ObjectiveStateRow } from "../lib/learnerState";

/** How one learner stood on each objective: the band it put them in, and why. */
export function LearnerStateTable({
  states,
  objectives,
}: {
  states: ObjectiveStateRow[];
  objectives: { id: string; text: string }[];
}) {
  if (states.length === 0) return <p className="text-sm text-(--muted)">No learner state kept.</p>;
  const text = new Map(objectives.map((objective) => [objective.id, objective.text]));
  return (
    <div className="overflow-x-auto">
      <table className={TABLE}>
        <thead>
          <tr>
            <th className={`${TH} w-1/2`}>Objective</th>
            <th className={TH}>Band</th>
            <th className={TH}>Evidence</th>
          </tr>
        </thead>
        <tbody>
          {states.map((state) => (
            <tr key={state.objectiveId}>
              <td className={ROW_HEAD}>{text.get(state.objectiveId) ?? state.objectiveId}</td>
              <td className={`${TD} capitalize`}>{state.band ?? "—"}</td>
              <td className={`${TD} text-(--ink-2)`}>
                {state.mastery ?? "—"}
                {state.misconception ? (
                  <p className="text-xs text-(--muted)">{state.misconception}</p>
                ) : null}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
