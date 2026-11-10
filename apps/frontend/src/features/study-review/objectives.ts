import type { LearnerClasswork } from "@/features/study-classwork/types";
import type { ComparePackManifest, ComparePackStep } from "@/features/experiments/lib/experiments";
import type { LessonStepStructured, PracticeBlock } from "@/shared/types/lesson-schema";

/**
 * A lesson taken objective by objective, as the study's rating documents took it: what the
 * teacher taught for the objective, and the evaluation questions she set on it.
 */
export type LessonObjective = {
  id: string;
  text: string;
  curriculumTarget: string | null;
  /** The plan's core steps that teach it. */
  steps: LessonStepStructured[];
  /** The teacher's evaluation questions tagged to it. */
  questions: PracticeBlock[];
};

type PlanObjective = {
  lesson_objective_id: string;
  objective_text: string;
  objective_order?: number;
  curriculum_objective_text?: string | null;
};

type Plan = { steps: LessonStepStructured[]; lesson_plan_objectives?: PlanObjective[] | null };

const isPractice = (block: { type: string }): block is PracticeBlock => block.type === "practice";

/** A step's kind, under the name the lesson-plan endpoint sends or the stored one. */
const kindOf = (step: LessonStepStructured) => step.step_role ?? step.step_kind;

/** The plan's objectives in order, each with the steps that teach it and its questions. */
export function lessonObjectives(plan: Plan): LessonObjective[] {
  const objectives = [...(plan.lesson_plan_objectives ?? [])].sort(
    (a, b) => (a.objective_order ?? 0) - (b.objective_order ?? 0)
  );
  const questions = plan.steps
    .filter((step) => kindOf(step) === "evaluation")
    .flatMap((step) => (step.blocks ?? []).filter(isPractice));
  return objectives.map((objective) => ({
    id: objective.lesson_objective_id,
    text: objective.objective_text,
    curriculumTarget: objective.curriculum_objective_text ?? null,
    steps: plan.steps.filter(
      (step) => kindOf(step) === "core" && step.lesson_objective_id === objective.lesson_objective_id
    ),
    questions: questions.filter(
      (question) => question.lesson_objective_id === objective.lesson_objective_id
    ),
  }));
}

/** The note's sections for one objective, in the note's order. */
export function sectionsFor(
  manifest: ComparePackManifest | undefined,
  objectiveId: string
): ComparePackStep[] {
  return (manifest?.steps ?? []).filter((step) => step.lesson_objective_id === objectiveId);
}

/**
 * The objectives a Part 2 set compared: those the learner has marked class work for. Across all
 * 26 of the study's learner cases this is exactly the set each rating document compared.
 */
export function comparedObjectives(
  objectives: LessonObjective[],
  classwork: LearnerClasswork | undefined
): Set<string> {
  const marked = new Set(
    (classwork?.script?.answers ?? [])
      .filter((answer) => answer.mark !== "unmarked")
      .map((answer) => answer.n)
  );
  const objectivesMarked = new Set(
    (classwork?.questions ?? [])
      .filter((question) => marked.has(question.n))
      .map((question) => question.lesson_objective_id)
  );
  return new Set(objectives.map((o) => o.id).filter((id) => objectivesMarked.has(id)));
}
