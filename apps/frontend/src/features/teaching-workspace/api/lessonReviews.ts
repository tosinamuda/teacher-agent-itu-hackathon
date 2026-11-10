import { apiFetch } from "@/shared/api/client";

/** What waits for the teacher in one lesson. */
export type LessonReview = {
  lesson_period_id: string;
  plans_to_approve: number;
  materials_to_review: number;
  notes_to_review: number;
  /** `plan`, or the type of the material that has waited longest. */
  oldest_kind: string;
  waiting_since: string;
};

/** The lessons of the workspace's subject that have something waiting; the others are left out. */
export const listLessonReviews = (
  workspaceId: string,
): Promise<LessonReview[]> =>
  apiFetch<{ lessons: LessonReview[] }>(
    `/teaching/workspaces/${workspaceId}/lesson-reviews`,
  ).then((response) => response.lessons);
