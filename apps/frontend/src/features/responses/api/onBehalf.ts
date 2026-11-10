import { apiFetch } from "@/shared/api/client";

export type OnBehalfObjective = {
  lesson_objective_id: string;
  objective_text?: string | null;
};

export type OnBehalfItem = {
  item_id: string;
  lesson_objective_id?: string | null;
  stem: string;
  options: Record<string, string>;
};

export type OnBehalfContext = {
  plan_version_id: string;
  subject?: string | null;
  topic?: string | null;
  subtopic?: string | null;
  objectives: OnBehalfObjective[];
  items: OnBehalfItem[];
  submitted_student_ids: string[];
};

export type ManualObjectiveScore = {
  lesson_objective_id: string;
  score: number;
  max_score: number;
};

export type OnBehalfAnswer = { item_id: string; selected_option: string };

export type Mark = "correct" | "incorrect" | "unmarked";

/** One question of classwork that is not multiple choice, and how a student's work was marked. */
export type MarkedWork = {
  lesson_objective_id: string;
  question: string;
  model_answer: string;
  mark: Mark;
  working: string;
  misconception_code: string | null;
  misconception_why: string | null;
};

export type OnBehalfRequest = {
  student_id: string;
  answers?: OnBehalfAnswer[];
  objective_scores?: ManualObjectiveScore[];
  marked_work?: MarkedWork[];
  provenance_attachment_id?: string | null;
};

export type OnBehalfResult = {
  diagnostic_id: string;
  student_id: string;
  plan_version_id: string;
  objectives_scored: number;
};

export const fetchOnBehalfContext = (planVersionId: string): Promise<OnBehalfContext> =>
  apiFetch<OnBehalfContext>(
    `/assessments/exit-assessment/${encodeURIComponent(planVersionId)}/responses/manual/context`
  );

export const enterOnBehalfResponses = (
  planVersionId: string,
  request: OnBehalfRequest
): Promise<OnBehalfResult> =>
  apiFetch<OnBehalfResult>(
    `/assessments/exit-assessment/${encodeURIComponent(planVersionId)}/responses/manual`,
    { method: "POST", body: JSON.stringify(request) }
  );
