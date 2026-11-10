import type {
  LessonStepStructured,
  ContentBlock,
} from "@/shared/types/lesson-schema";

import type { SessionPlanData } from "../components/SessionPlanView";

/** One thing that differs between two versions, as the words each version has. */
export type FieldChange = { label: string; before: string; after: string };

export type StepChange = {
  stepId: string;
  title: string;
  kind: "added" | "removed" | "changed";
  changes: FieldChange[];
};

export type PlanDiff = { overall: FieldChange[]; steps: StepChange[] };

const bullets = (lines: string[]): string =>
  lines.map((line) => `• ${line}`).join("\n");

function describeBlock(block: ContentBlock): string {
  switch (block.type) {
    case "explanation":
      return block.content;
    case "practice":
      return `Question: ${block.question} Answer: ${block.answer}`;
    case "worked_example":
      return `${block.problem} ${block.steps.map((step) => step.content).join(" ")} ${block.final_answer}`.trim();
    case "visual":
      return block.caption ?? "A drawing";
  }
}

/** The words of a step, one labelled field at a time, so two steps can be set beside each other. */
function stepFields(step: LessonStepStructured): Record<string, string> {
  const activities = step.activities ?? [];
  const minutes = step.duration_minutes ?? step.estimated_minutes;
  return {
    Title: step.title,
    Time: minutes === undefined ? "" : `${minutes} min`,
    Teacher: bullets(
      activities.filter((a) => a.who === "teacher").map((a) => a.what),
    ),
    Students: bullets(
      activities.filter((a) => a.who === "student").map((a) => a.what),
    ),
    Notes: step.content ?? "",
    Content: (step.blocks ?? []).map(describeBlock).join("\n"),
  };
}

function changedFields(
  before: Record<string, string>,
  after: Record<string, string>,
): FieldChange[] {
  return Object.keys(after)
    .filter((label) => (before[label] ?? "") !== after[label])
    .map((label) => ({
      label,
      before: before[label] ?? "",
      after: after[label],
    }));
}

function planFields(plan: SessionPlanData): Record<string, string> {
  return {
    Objectives: bullets(
      (plan.lesson_plan_objectives ?? []).map(
        (objective) => objective.objective_text,
      ),
    ),
    "Students already know": bullets(plan.entry_behaviour ?? []),
    Materials: bullets(plan.instructional_materials ?? []),
    Sources: bullets(plan.references ?? []),
  };
}

/** What changed from one version of a plan to another: the plan's basis, then step by step. */
export function diffPlans(
  before: SessionPlanData,
  after: SessionPlanData,
): PlanDiff {
  const beforeSteps = new Map(before.steps.map((step) => [step.step_id, step]));
  const afterIds = new Set(after.steps.map((step) => step.step_id));
  const steps: StepChange[] = [];

  for (const step of after.steps) {
    const was = beforeSteps.get(step.step_id);
    if (!was) {
      steps.push({
        stepId: step.step_id,
        title: step.title,
        kind: "added",
        changes: changedFields({}, stepFields(step)).filter(
          (change) => change.after !== "",
        ),
      });
      continue;
    }
    const changes = changedFields(stepFields(was), stepFields(step));
    if (changes.length > 0)
      steps.push({
        stepId: step.step_id,
        title: step.title,
        kind: "changed",
        changes,
      });
  }
  for (const step of before.steps) {
    if (!afterIds.has(step.step_id)) {
      steps.push({
        stepId: step.step_id,
        title: step.title,
        kind: "removed",
        changes: [],
      });
    }
  }
  return {
    overall: changedFields(planFields(before), planFields(after)),
    steps,
  };
}

export const isUnchanged = (diff: PlanDiff): boolean =>
  diff.overall.length === 0 && diff.steps.length === 0;
