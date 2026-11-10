const REASONS: [string, string][] = [
  [
    "lesson_plan_is_frozen_into_a_running_study",
    "A running study froze this plan, so it cannot be changed.",
  ],
  ["lesson_plan_is_already_closed", "This plan is already closed."],
  [
    "lesson_plan_changed_since_it_was_reviewed",
    "The plan changed since you opened it. Open the current version and try again.",
  ],
  [
    "concluded",
    "This lesson's study has concluded, so its plan can no longer change.",
  ],
];

/** Why discarding a plan or taking its approval back was refused, as a teacher reads it. */
export function closingError(error: Error | null): string | null {
  if (!error) return null;
  const found = REASONS.find(([code]) => error.message.includes(code));
  return found ? found[1] : "It could not be done. Try again.";
}
