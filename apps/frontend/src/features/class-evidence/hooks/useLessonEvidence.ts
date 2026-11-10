import { useQuery } from "@tanstack/react-query";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { arrangeLearners } from "@/features/learners/lib/arrangeLearners";
import type { ClassLearnersResponse } from "@/features/learners/types";
import { apiFetch } from "@/shared/api/client";

/** How each learner of the class did on one lesson's class test, those who need the most help first. */
export function useLessonEvidence(lessonPeriodId: string) {
  const { currentWorkspace } = useTeachingWorkspace();
  const workspaceId = currentWorkspace?.id ?? "";

  const query = useQuery({
    queryKey: ["lesson-evidence", workspaceId, lessonPeriodId],
    queryFn: () =>
      apiFetch<ClassLearnersResponse>(`/teaching/workspaces/${workspaceId}/lessons/${lessonPeriodId}/evidence`),
    enabled: Boolean(workspaceId && lessonPeriodId),
  });

  return { ...query, learners: arrangeLearners(query.data?.learners ?? [], "") };
}
