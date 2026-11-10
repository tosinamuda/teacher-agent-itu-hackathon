/**
 * A focal learner's state per objective, from the snapshot an H2 execution kept.
 *
 * The app keeps the learner state it built (`objective_states`, one entry per objective).
 * An imported study keeps what its generator read: a map from objective id to that
 * objective's state. Both are read here, so a snapshot is never shown as raw JSON.
 */

export type ObjectiveStateRow = {
  objectiveId: string;
  band: string | null;
  mastery: string | null;
  misconception: string | null;
};

type Json = Record<string, unknown>;

const isObject = (value: unknown): value is Json =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const text = (value: unknown): string | null =>
  typeof value === "string" && value.trim() ? value : null;

function misconception(value: unknown): string | null {
  if (isObject(value)) return text(value.description) ?? text(value.code);
  return text(value);
}

function fromAppState(state: Json): ObjectiveStateRow {
  const correct = state.questions_correct;
  const total = state.questions_total;
  const mastery =
    typeof correct === "number" && typeof total === "number"
      ? `${correct} of ${total} correct`
      : null;
  return {
    objectiveId: String(state.lesson_objective_id ?? ""),
    band: text(state.band),
    mastery,
    misconception: text(state.misconception_description) ?? text(state.misconception_code),
  };
}

function fromStudyState(objectiveId: string, state: Json): ObjectiveStateRow {
  return {
    objectiveId: text(state.lesson_objective_id) ?? objectiveId,
    band: text(state.mastery_band),
    mastery: text(state.mastery),
    misconception: misconception(state.misconception),
  };
}

export function objectiveStates(snapshot: unknown): ObjectiveStateRow[] {
  if (!isObject(snapshot)) return [];
  if (Array.isArray(snapshot.objective_states)) {
    return snapshot.objective_states.filter(isObject).map(fromAppState);
  }
  return Object.entries(snapshot)
    .filter((entry): entry is [string, Json] => isObject(entry[1]))
    .map(([objectiveId, state]) => fromStudyState(objectiveId, state));
}
