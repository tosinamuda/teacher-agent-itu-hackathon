import { useQuery } from "@tanstack/react-query";

import { getReviewLessonPlan } from "../api/lessonPlan";

/**
 * Fetch the authored lesson plan behind a revision note (by its plan version id),
 * lazily — only when `enabled` (i.e. the teacher opens the comparison view).
 */
export const useReviewLessonPlan = (planVersionId: string, enabled: boolean) =>
  useQuery({
    queryKey: ["reviewLessonPlan", planVersionId],
    queryFn: () => getReviewLessonPlan(planVersionId),
    enabled: enabled && Boolean(planVersionId),
  });
