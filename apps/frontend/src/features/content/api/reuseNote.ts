import { apiFetch } from "@/shared/api/client";

/** Copy a lesson note onto a plan with the same steps; it waits for the teacher's review. */
export const reuseLessonNote = (
  sourceContentId: string,
  planVersionId: string,
): Promise<{ content_id: string }> =>
  apiFetch<{ content_id: string }>("/content/reuse-note", {
    method: "POST",
    body: JSON.stringify({
      source_content_id: sourceContentId,
      plan_version_id: planVersionId,
    }),
  });
