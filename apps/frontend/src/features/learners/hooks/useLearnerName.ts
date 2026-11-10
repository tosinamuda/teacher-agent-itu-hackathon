import { useQuery } from "@tanstack/react-query";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";

import { classLearnersQuery } from "../lib/classLearnersQuery";

/** The name of a learner of the class the teacher has open; null until it loads, or when they are not in it. */
export function useLearnerName(studentId: string | null): string | null {
  const { currentWorkspace } = useTeachingWorkspace();
  const learners = useQuery({
    ...classLearnersQuery(currentWorkspace?.id ?? ""),
    enabled: Boolean(studentId && currentWorkspace?.id),
  });
  return learners.data?.learners.find((learner) => learner.student_id === studentId)?.full_name ?? null;
}
