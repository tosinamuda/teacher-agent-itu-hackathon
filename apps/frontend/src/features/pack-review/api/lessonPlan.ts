import { apiFetch } from "@/shared/api/client";
import { ContentBlock } from "@/shared/types/lesson-schema";

/** One objective the lesson plan set for the lesson. */
export type ReviewLessonObjective = {
  lesson_objective_id?: string | null;
  objective_text?: string | null;
};

/** One authored teaching step (intro / core / evaluation) with its content blocks. */
export type ReviewLessonStep = {
  title?: string | null;
  step_role?: string | null;
  step_kind?: string | null;
  lesson_objective_id?: string | null;
  blocks: ContentBlock[];
};

/** The authored lesson plan, as needed to compare against the generated revision note. */
export type ReviewLessonPlan = {
  topic?: string | null;
  subtopic?: string | null;
  lesson_plan_objectives: ReviewLessonObjective[];
  steps: ReviewLessonStep[];
};

type LessonPlanResponse = { session_plan: ReviewLessonPlan };

/**
 * Fetch the authored lesson plan for a revision note's plan version, so the teacher
 * can compare the plan against the generated note. Accepts a plan id or version id.
 */
export const getReviewLessonPlan = async (
  planVersionId: string,
): Promise<ReviewLessonPlan> => {
  const data = await apiFetch<LessonPlanResponse>(
    `/artefacts/lesson-plans/${encodeURIComponent(planVersionId)}`,
  );
  return data.session_plan;
};
