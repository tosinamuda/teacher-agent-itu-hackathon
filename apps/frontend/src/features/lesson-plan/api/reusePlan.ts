import { apiFetch } from "@/shared/api/client";

/** A lesson objective that needs a curriculum objective chosen for it. */
export type UnmappedObjective = {
  lesson_objective_id: string;
  objective_text: string;
};

/** A curriculum objective of the lesson to point a lesson objective at. */
export type CurriculumChoice = {
  curriculum_objective_id: string;
  objective_text: string;
};

/** What reusing a plan answers: it is saved, or these choices are still to make. */
export type PlanReuseResult =
  | { status: "reused" }
  | {
      status: "needs_curriculum_choice";
      unmapped: UnmappedObjective[];
      choices: CurriculumChoice[];
    };

/** The plan to reuse: a saved plan version, or a plan's content. */
export type PlanSource =
  | { kind: "version"; planVersionId: string }
  | { kind: "file"; sessionPlan: Record<string, unknown>; fileName: string };

/**
 * Reuse an existing plan as the experiment's plan. The server keeps the plan's content, points
 * each lesson objective at a curriculum objective of this lesson, and saves it as a draft.
 */
export const reuseExperimentPlan = (
  experimentId: string,
  source: PlanSource,
  curriculumChoices: Record<string, string>,
): Promise<PlanReuseResult> =>
  apiFetch<PlanReuseResult>(
    `/experiments/${encodeURIComponent(experimentId)}/plan/reuse`,
    {
      method: "POST",
      body: JSON.stringify({
        ...(source.kind === "version"
          ? { source_plan_version_id: source.planVersionId }
          : { session_plan: source.sessionPlan }),
        curriculum_choices: curriculumChoices,
      }),
    },
  );

/** What reusing a plan on a lesson answers: the saved draft, or the choices still to make. */
export type LessonPlanReuseResult =
  | { status: "reused"; plan: { plan_id: string; version_id: string } }
  | {
      status: "needs_curriculum_choice";
      unmapped: UnmappedObjective[];
      choices: CurriculumChoice[];
    };

/**
 * Use an existing plan as this lesson's plan. It is saved as a draft, naming where it came from,
 * for the teacher to read through and accept.
 */
export const reuseLessonPlan = (
  lessonPeriodId: string,
  source: PlanSource,
  curriculumChoices: Record<string, string>,
): Promise<LessonPlanReuseResult> =>
  apiFetch<LessonPlanReuseResult>("/artefacts/lesson-plans/reuse", {
    method: "POST",
    body: JSON.stringify({
      session_id: lessonPeriodId,
      ...(source.kind === "version"
        ? { source_plan_version_id: source.planVersionId }
        : { session_plan: source.sessionPlan }),
      curriculum_choices: curriculumChoices,
    }),
  });
