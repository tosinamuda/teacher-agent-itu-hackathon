import { useQuery } from "@tanstack/react-query";

import { listLessonReviews, type LessonReview } from "../api/lessonReviews";

const NONE: LessonReview[] = [];

/** What waits for the teacher in each lesson of the workspace's subject. */
export function useLessonReviews(workspaceId: string | null) {
  const query = useQuery({
    queryKey: ["lessonReviews", workspaceId ?? "empty"],
    queryFn: () => listLessonReviews(workspaceId ?? ""),
    enabled: Boolean(workspaceId),
  });
  return { reviews: query.data ?? NONE };
}
