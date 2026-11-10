import type { EditableSessionPlan } from "../api/manualEdit";

type Activity = { who: string; what: string };
type Step = {
  step_id: string;
  title: string;
  content: string;
  estimated_minutes?: number | null;
  activities?: Activity[];
};
type Objective = { lesson_objective_id: string; objective_text: string };

const stepsOf = (plan: EditableSessionPlan): Step[] =>
  (plan.steps ?? []) as unknown as Step[];
const objectivesOf = (plan: EditableSessionPlan): Objective[] =>
  (plan.lesson_plan_objectives ?? []) as unknown as Objective[];

const wordsOf = (step: Step): string =>
  JSON.stringify([
    step.title,
    step.content,
    step.estimated_minutes ?? null,
    (step.activities ?? []).map((activity) => [activity.who, activity.what]),
  ]);

/** The steps whose title, minutes, content or activities differ from what the plan had. */
export function editedStepIds(
  before: EditableSessionPlan,
  after: EditableSessionPlan,
): string[] {
  const was = new Map(
    stepsOf(before).map((step) => [step.step_id, wordsOf(step)]),
  );
  return stepsOf(after)
    .filter((step) => was.get(step.step_id) !== wordsOf(step))
    .map((step) => step.step_id);
}

const LISTS = [
  "entry_behaviour",
  "instructional_materials",
  "references",
] as const;

/** How many things differ: each changed objective, step and list counts once. */
export function changeCount(
  before: EditableSessionPlan,
  after: EditableSessionPlan,
): number {
  const was = new Map(
    objectivesOf(before).map((o) => [o.lesson_objective_id, o.objective_text]),
  );
  const objectives = objectivesOf(after).filter(
    (objective) =>
      was.get(objective.lesson_objective_id) !== objective.objective_text,
  ).length;
  const lists = LISTS.filter(
    (key) =>
      JSON.stringify(before[key] ?? []) !== JSON.stringify(after[key] ?? []),
  ).length;
  return objectives + lists + editedStepIds(before, after).length;
}
