import { PlanObjective } from "../types";

/** How a question names the objective it tests: its number in the plan, and its text. */
export function objectiveLabel(objectives: PlanObjective[], objectiveId: string): string | null {
  const index = objectives.findIndex((o) => o.lesson_objective_id === objectiveId);
  if (index < 0) return null;
  const objective = objectives[index];
  return `Objective ${objective.objective_order ?? index + 1}: ${objective.objective_text}`;
}
