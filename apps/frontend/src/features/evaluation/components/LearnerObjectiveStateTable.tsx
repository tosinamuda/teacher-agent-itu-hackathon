import { misconceptionText } from "../services/raterPresentation";
import { EvaluationObjectiveState } from "../types";

/**
 * Friendly rater-facing labels for the assigned-band enum
 * (`remediate` / `reinforce` / `extend`). The thesis taxonomy is hidden
 * from raters; they see the suggested study direction in plain English.
 */
const BAND_LABELS: Record<string, string> = {
  remediate: "Needs more practice",
  reinforce: "On track",
  extend: "Ready for extension",
};

/** Rater-friendly labels for low/medium/high signal enums. */
const SIGNAL_LABELS: Record<string, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
};

function friendlyBand(band: string | null | undefined): string {
  if (!band) return "—";
  return BAND_LABELS[band.toLowerCase()] ?? band;
}

function friendlySignal(value: string | null | undefined): string {
  if (!value) return "—";
  return SIGNAL_LABELS[value.toLowerCase()] ?? value;
}

function objectiveLabel(state: EvaluationObjectiveState, ordinal: number): string {
  const text = state.objective_text?.trim();
  return text ? `Objective ${ordinal}: ${text}` : `Objective ${ordinal}`;
}

/**
 * Render the per-objective learner-state card for the H2 worksheet.
 *
 * One row per lesson objective with the assigned study profile, confidence,
 * perceived difficulty, and any recorded misconception — the same evidence
 * the rater needs to judge whether the personalised version fits this
 * learner. Returns `null` when no per-objective state is on the wire
 * (the caller can keep the surrounding layout simple).
 */
export function LearnerObjectiveStateTable({
  states,
  title = "Per-objective learner state",
  hint = "What this learner needs, objective by objective. Use this to judge whether the learner version fits.",
}: {
  states: EvaluationObjectiveState[] | undefined;
  title?: string;
  hint?: string;
}) {
  if (!states || states.length === 0) return null;
  return (
    <div className="space-y-3 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] p-4">
      <div className="space-y-1">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
          {title}
        </p>
        <p className="text-xs leading-relaxed text-[color:var(--muted)]">{hint}</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm text-[color:var(--ink)]">
          <thead>
            <tr className="border-b border-[color:var(--line)] text-left text-xs font-semibold uppercase tracking-[0.12em] text-[color:var(--muted)]">
              <th className="py-2 pr-3">Objective</th>
              <th className="px-3 py-2">Profile</th>
              <th className="px-3 py-2">Confidence</th>
              <th className="px-3 py-2">Difficulty</th>
              <th className="pl-3 py-2">Misconception</th>
            </tr>
          </thead>
          <tbody>
            {states.map((state, index) => (
              <tr
                key={state.lesson_objective_id}
                className="border-b border-[color:var(--line)] align-top last:border-b-0"
              >
                <td className="py-3 pr-3 leading-snug">{objectiveLabel(state, index + 1)}</td>
                <td className="px-3 py-3 font-medium">{friendlyBand(state.band)}</td>
                <td className="px-3 py-3">{friendlySignal(state.confidence)}</td>
                <td className="px-3 py-3">{friendlySignal(state.perceived_difficulty)}</td>
                <td className="pl-3 py-3 leading-snug">
                  {misconceptionText(state) ?? "None recorded"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
