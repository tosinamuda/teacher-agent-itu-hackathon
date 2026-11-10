import { useQuery } from "@tanstack/react-query";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { apiFetch } from "@/shared/api/client";
import { LearnerResults } from "../types";

/** A learner's class tests and per-objective results for the class the teacher has open. */
export function useLearnerResults(studentId: string) {
  const { currentWorkspace } = useTeachingWorkspace();
  const workspaceId = currentWorkspace?.id ?? "";

  return useQuery({
    queryKey: ["learner-results", workspaceId, studentId],
    queryFn: () =>
      apiFetch<LearnerResults>(
        `/teaching/workspaces/${workspaceId}/learners/${encodeURIComponent(studentId)}/results`,
      ),
    enabled: Boolean(workspaceId && studentId),
  });
}
