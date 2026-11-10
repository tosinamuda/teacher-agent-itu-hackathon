import { useQueries } from "@tanstack/react-query";

import { listLessonReviews } from "../api/lessonReviews";

/** How many things wait for the teacher in each class, by workspace id. */
export function useWaitingByClass(
  workspaceIds: string[],
): Record<string, number> {
  const results = useQueries({
    queries: workspaceIds.map((id) => ({
      queryKey: ["lessonReviews", id],
      queryFn: () => listLessonReviews(id),
    })),
  });
  return Object.fromEntries(
    workspaceIds.map((id, at) => [
      id,
      (results[at].data ?? []).reduce(
        (sum, lesson) =>
          sum +
          lesson.plans_to_approve +
          lesson.materials_to_review +
          lesson.notes_to_review,
        0,
      ),
    ]),
  );
}
